import argparse
import glob
import itertools
import multiprocessing
from typing import List, Union

import numpy as np

from eval_plus.evaluation.evaluate_helpers import (
    TimeoutException,
    create_tempdir,
    reliability_guard,
    swallow_io,
    time_limit,
)
from eval_plus.input_generation.mut_gen import MutateGen
from eval_plus.utils import get_human_eval_plus


# unbiased estimator from https://github.com/openai/human-eval
def estimate_pass_at_k(
    num_samples: Union[int, List[int], np.ndarray],
    num_correct: Union[List[int], np.ndarray],
    k: int,
) -> np.ndarray:
    """
    Estimates pass@k of each problem and returns them in an array.
    """

    def estimator(n: int, c: int, k: int) -> float:
        """
        Calculates 1 - comb(n - c, k) / comb(n, k).
        """
        if n - c < k:
            return 1.0
        return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

    if isinstance(num_samples, int):
        num_samples_it = itertools.repeat(num_samples, len(num_correct))
    else:
        assert len(num_samples) == len(num_correct)
        num_samples_it = iter(num_samples)

    return np.array(
        [estimator(int(n), int(c), k) for n, c in zip(num_samples_it, num_correct)]
    )


# hacky way to handle \n\r, etc in strings
def to_raw(string):
    return string.encode("unicode-escape").decode().replace("\\\\", "\\")


def construct_inputs_sig(inputs: list) -> str:
    str_builder = ""
    for x in inputs:
        if type(x) == str:
            str_builder += f"'{to_raw(x)}',"
        else:
            str_builder += f"{x},"
    return str_builder[:-1]


def execute(code: str, inputs: List, signature: str) -> str:
    eval_code = code + f"\noutputs = {signature}({construct_inputs_sig(inputs)})"

    def unsafe_execute():
        with create_tempdir():
            # These system calls are needed when cleaning up tempdir.
            import os
            import shutil

            rmtree = shutil.rmtree
            rmdir = os.rmdir
            chdir = os.chdir
            # Disable functionalities that can make destructive changes to the test.
            reliability_guard()
            # Construct the check program and run it.
            check_program = eval_code
            exec_globals = {}
            try:
                with swallow_io():
                    with time_limit(1):
                        exec(check_program, exec_globals)
                result.append(exec_globals["outputs"])
            except TimeoutException:
                result.append("timed out")
            except BaseException as e:
                result.append("thrown exception")
            # Needed for cleaning up.
            shutil.rmtree = rmtree
            os.rmdir = rmdir
            os.chdir = chdir

    manager = multiprocessing.Manager()
    result = manager.list()
    p = multiprocessing.Process(target=unsafe_execute)
    p.start()
    p.join(timeout=1 + 1)
    if p.is_alive():
        p.kill()
    return result[0]


def evaluate_files(files: List[str], inputs, outputs, entry_point: str) -> List[str]:
    suc_files = []
    for file in files:
        code = open(file, "r").read()
        suc = True
        for input, output in zip(inputs, outputs):
            o = execute(code, input, entry_point)
            if o != output:
                suc = False
                break
        if suc:
            suc_files.append(file)
    return suc_files


def evaluate(args, problems):
    base_total, base_correct, new_correct = [], [], []
    for problem in problems:
        p_name = problem["task_id"].replace("/", "_")
        print("evaluating for {} ...".format(p_name))
        # first populate the gd results
        gd_results = []
        code = problem["prompt"] + problem["canonical_solution"]
        for base_input in problem["base_input"]:
            o = execute(code, base_input, problem["entry_point"])
            # sanity
            assert o != "timed out" and o != "thrown exception"
            gd_results.append(o)

        gen_files = glob.glob(args.r_folder + f"/{p_name}/*.py")
        base_suc_files = evaluate_files(
            gen_files, problem["base_input"], gd_results, problem["entry_point"]
        )
        print(f"Total Gen: {len(gen_files)}, Base Success Files: {len(base_suc_files)}")
        base_total.append(len(gen_files))
        base_correct.append(len(base_suc_files))

        if args.more_eval:
            input_gen = MutateGen(problem["base_input"]).generate(100)
            new_inputs, gd_new_results = [], []
            for new_input in input_gen:
                o = execute(code, new_input, problem["entry_point"])
                if o != "timed out" and o != "thrown exception":
                    new_inputs.append(new_input)
                    gd_new_results.append(o)
            new_suc_files = evaluate_files(
                base_suc_files, new_inputs, gd_new_results, problem["entry_point"]
            )
            print(
                f"Total Gen: {len(gen_files)}, New Success Files: {len(new_suc_files)}"
            )
            new_correct.append(len(new_suc_files))

    # Calculate pass@k.
    total = np.array(base_total)
    correct = np.array(base_correct)
    new_correct = np.array(new_correct)
    pass_at_k = {
        f"pass@{k}": estimate_pass_at_k(total, correct, k).mean()
        for k in [1, 10, 100]
        if (total >= k).all()
    }
    print(pass_at_k)
    pass_at_k = {
        f"pass@{k}": estimate_pass_at_k(total, new_correct, k).mean()
        for k in [1, 10, 100]
        if (total >= k).all()
    }
    print(pass_at_k)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True, type=str)
    parser.add_argument("--r_folder", required=True, type=str)
    parser.add_argument("--more_eval", action="store_true")
    args = parser.parse_args()

    if args.dataset not in ["humaneval"]:
        raise NotImplementedError("Unsupported dataset: {}".format(args.dataset))

    problems = get_human_eval_plus()
    evaluate(args, problems)


if __name__ == "__main__":
    main()

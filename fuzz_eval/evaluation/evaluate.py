import argparse
import glob
import itertools
import multiprocessing
from typing import Dict, List, Union

import numpy as np

from fuzz_eval.evaluation.evaluate_helpers import (
    TimeoutException,
    create_tempdir,
    reliability_guard,
    swallow_io,
    time_limit,
)
from fuzz_eval.utils import get_fuzz_eval


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


def construct_inputs_sig(inputs: list) -> str:
    str_builder = ""
    for x in inputs:
        if type(x) == str:
            str_builder += f"'{x}',"
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
    base_total, base_correct = [], []
    for problem in problems:
        if (
            problem["reference"].strip().startswith("pass")
            or "32" in problem["task_id"]
        ):
            # gd not available.
            continue
        p_name = problem["task_id"].replace("/", "_")
        print("evaluating for {} ...".format(p_name))
        # first populate the gd results
        gd_results = []
        code = problem["prompt"] + problem["reference"]
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
            # where we would apply the additional testcases.
            raise NotImplementedError("More evaluation has not been implemented")

    # Calculate pass@k.
    total = np.array(base_total)
    correct = np.array(base_correct)
    pass_at_k = {
        f"pass@{k}": estimate_pass_at_k(total, correct, k).mean()
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

    problems = get_fuzz_eval()
    evaluate(args, problems)


if __name__ == "__main__":
    main()

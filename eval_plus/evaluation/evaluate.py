import argparse
import glob
import itertools
import json
import math
import multiprocessing
import os
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, List, Union

import numpy as np
from tqdm import tqdm

from eval_plus.evaluation.evaluate_helpers import (
    TimeoutException,
    create_tempdir,
    reliability_guard,
    swallow_io,
    time_limit,
)
from eval_plus.utils import get_human_eval_plus, get_human_eval_plus_inputs, to_raw

DEBUG = os.environ.get("DEBUG", False)


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
            str_builder += f"'{to_raw(x)}',"
        else:
            str_builder += f"{x},"
    return str_builder[:-1]


# oracle for 032
def poly(xs: list, x: float):
    """
    Evaluates polynomial with coefficients xs at point x.
    return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n
    """
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])


def batch_exec(
    code: str,
    inputs: List[Any],
    entry_point: str,
    fast_check: bool = False,
    expected=None,
    atol=None,
) -> Union[List[Any], bool]:
    if fast_check and expected:
        assert atol is not None
        assert len(inputs) == len(expected)

    timeout_unit = 1
    timeout = len(inputs) * timeout_unit

    def is_floats(x) -> bool:
        # check if it is float; List[float]; Tuple[float]
        if isinstance(x, float):
            return True
        if isinstance(x, (list, tuple)):
            return all(isinstance(i, float) for i in x)
        if isinstance(x, np.ndarray):
            return x.dtype == np.float64 or x.dtype == np.float32
        return False

    def unsafe_execute(atol):
        with create_tempdir():
            # These system calls are needed when cleaning up tempdir.
            import os
            import shutil

            rmtree = shutil.rmtree
            rmdir = os.rmdir
            chdir = os.chdir
            # Disable functionalities that can make destructive changes to the test.
            reliability_guard()
            exec_globals = {}
            try:
                with swallow_io():
                    with time_limit(timeout + 1):
                        exec(code, exec_globals)
                        fn = exec_globals[entry_point]
                        for i, inp in enumerate(inputs):
                            with time_limit(timeout_unit):
                                out = fn(*inp)

                            # slow mode: get all results
                            if not fast_check:
                                outputs.append(out)

                            # fast mode: check if the result is correct
                            if expected:
                                exp = expected[i]
                                exact_match = out == exp

                                if "find_zero" == entry_point:
                                    assert poly(*out, inp) <= atol

                                if atol == 0 and is_floats(exp):
                                    atol = 1e-6  # enforce atol for float comparison
                                if not exact_match and atol != 0:
                                    np.testing.assert_allclose(out, exp, atol=atol)
                                else:
                                    assert exact_match

                result.append("success")
            except TimeoutException:
                result.append(f"timed out :: {entry_point}")
                print(f"timed out :: {entry_point}")
            except BaseException:
                result.append("failed")
                if DEBUG:
                    traceback.print_exc()
            # Needed for cleaning up.
            shutil.rmtree = rmtree
            os.rmdir = rmdir
            os.chdir = chdir

    manager = multiprocessing.Manager()
    outputs = manager.list()
    result = manager.list()
    p = multiprocessing.Process(target=unsafe_execute, args=(atol,))
    p.start()
    p.join(timeout=timeout + 1)
    if p.is_alive():
        p.kill()

    if not result:
        result.append("timed out")

    if fast_check:
        return result[0] == "success"

    # cannot return outputs where inputs are invalid
    assert result[0] == "success"
    return outputs


def evaluate_files(
    files: List[str], inputs: List, expected: List, entry_point: str, atol: float
) -> List[str]:
    suc_files = []
    cache = {}
    for file in files:
        code = open(file, "r").read()
        if code in cache and cache[code]:
            suc_files.append(file)  # pass
            continue

        suc = batch_exec(
            code, inputs, entry_point, fast_check=True, expected=expected, atol=atol
        )

        if suc:
            suc_files.append(file)
        cache[code] = suc
    return suc_files


def evaluate_one(problem: dict, r_folder: str, more_eval: bool, iextra=None):
    p_name = problem["task_id"].replace("/", "_")
    print(
        "evaluating for {} ...".format(p_name),
        problem["atol"] if problem["atol"] else "",
    )
    # first populate the gd results
    code = problem["prompt"] + problem["reference"]
    gd_results = batch_exec(code, problem["base_input"], problem["entry_point"])

    gen_files = glob.glob(r_folder + f"/{p_name}/*.py")
    base_suc_files = evaluate_files(
        gen_files,
        problem["base_input"],
        gd_results,
        problem["entry_point"],
        problem["atol"],
    )

    msg = f"{p_name} :: Total {len(gen_files)} :: Base Success {len(base_suc_files)}"

    if more_eval and iextra:
        new_inputs = iextra
        gd_new_results = batch_exec(code, iextra, problem["entry_point"])

        new_suc_files = evaluate_files(
            base_suc_files,
            new_inputs,
            gd_new_results,
            problem["entry_point"],
            problem["atol"],
        )
        print(msg + f" :: New Success {len(new_suc_files)}")
    else:
        # same passing.
        new_suc_files = base_suc_files
        print(msg)

    return p_name, gen_files, base_suc_files, new_suc_files


def evaluate(flags, problems, extra_inputs=None):
    base_total, base_correct, new_correct = [], [], []
    if flags.parallel is None:
        n_workers = max(1, multiprocessing.cpu_count() // 2)
    else:
        n_workers = flags.parallel

    result_path = os.path.join(flags.r_folder, "eval_results.json")

    if os.path.isfile(result_path) and not flags.i_just_wanna_run:
        print(f"Load from {flags.r_folder + '/eval_results.json'}")
        with open(result_path, "r") as f:
            results = json.load(f)
        base_total = [len(x["base_files"]) for _, x in results["eval"].items()]
        base_correct = [len(x["correct_files"]) for _, x in results["eval"].items()]
        new_correct = [len(x["ncorrect_files"]) for _, x in results["eval"].items()]
    else:
        results = {
            # TODO put some meta data here
            "extra_input_hash": hash(str(problems)),
            "eval": {}  # dict of each p_name with all files / base-succ / new-succ files
            # TODO: incorrect file failing test inputs
        }
        with ThreadPoolExecutor(max_workers=n_workers) as executor:
            futures = []
            for problem in problems:
                p_name = problem["task_id"].replace("/", "_")
                iextra = extra_inputs.get(p_name, None) if extra_inputs else None
                args = (problem, flags.r_folder, flags.more_eval, iextra)
                futures.append(executor.submit(evaluate_one, *args))
            for future in tqdm(as_completed(futures), total=len(futures)):
                p_name, btotal, bcorrect, ncorrect = future.result()
                results["eval"][p_name] = {
                    "base_files": btotal,
                    "correct_files": bcorrect,
                    "ncorrect_files": ncorrect,
                }
                base_total.append(len(btotal))
                base_correct.append(len(bcorrect))
                new_correct.append(len(ncorrect))

    if os.path.isfile(result_path):
        decision = ""
        while decision.lower() not in ["y", "n"]:
            print(f"{result_path} already exists. Press [Y/N] to overwrite or exit...")
            decision = input()

        if decision.lower() == "y":
            # mv the file to a backup
            new_path = result_path + ".bak"
            while os.path.isfile(new_path):
                new_path += ".bak"
            os.rename(result_path, new_path)
            print(f"Backup {result_path} to {new_path}")

    if not os.path.isfile(result_path):
        with open(result_path, "w") as f:
            json.dump(results, f)

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
    parser.add_argument("--parallel", default=None, type=int)
    parser.add_argument("--i-just-wanna-run", action="store_true")
    args = parser.parse_args()

    if args.dataset not in ["humaneval"]:
        raise NotImplementedError("Unsupported dataset: {}".format(args.dataset))

    problems = get_human_eval_plus()
    more_inputs = None
    if args.more_eval:
        more_inputs = get_human_eval_plus_inputs()

    evaluate(args, problems, more_inputs)


if __name__ == "__main__":
    main()

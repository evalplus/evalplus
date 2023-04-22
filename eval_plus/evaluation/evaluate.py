import argparse
import glob
import itertools
import json
import math
import multiprocessing
import os
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from typing import Any, List, Union

import numpy as np
from tqdm import tqdm

from eval_plus.evaluation.evaluate_helpers import (
    create_tempdir,
    reliability_guard,
    swallow_io,
    time_limit,
)
from eval_plus.input_generation.util import trusted_exec
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


SUCCESS = "success"
FAILED = "failed"
TIMEOUT = "timed out"


def untrusted_check(
    code: str,
    inputs: List[Any],
    entry_point: str,
    expected,
    atol,
    ref_time: List[float],
    fast_check: bool = False,
) -> Union[List[bool], bool]:
    time_limits = [max(0.5, 2 * t) for t in ref_time]
    timeout = sum(time_limits)

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
            # allow only 4GB memory usage
            maximum_memory_bytes = 4 * 1024 * 1024 * 1024
            reliability_guard(maximum_memory_bytes=maximum_memory_bytes)
            exec_globals = {}
            try:
                with swallow_io():
                    exec(code, exec_globals)
                    fn = exec_globals[entry_point]
                    for i, inp in enumerate(inputs):
                        try:
                            with time_limit(time_limits[i]):
                                out = fn(*inp)

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
                        except BaseException:
                            if fast_check:
                                raise
                            details.append(False)
                            continue

                        details.append(True)
                result.append(SUCCESS)
            except BaseException:
                result.append(FAILED)
            # Needed for cleaning up.
            shutil.rmtree = rmtree
            os.rmdir = rmdir
            os.chdir = chdir

    manager = multiprocessing.Manager()

    result = manager.list()
    details = manager.list()
    p = multiprocessing.Process(target=unsafe_execute, args=(atol,))
    p.start()
    p.join(timeout=timeout + 1)
    if p.is_alive():
        p.terminate()
        time.sleep(0.1)
    if p.is_alive():
        p.kill()
        time.sleep(0.1)
    p.close()

    if not result:
        result.append(TIMEOUT)

    if result[0] == SUCCESS:
        if len(details) != len(inputs) or not all(details):
            result[0] = FAILED

    if result[0] != SUCCESS:
        details = None

    return result[0], np.array(details)


def evaluate_files(
    files: List[str],
    inputs: List,
    expected: List,
    entry_point: str,
    atol: float,
    ref_time: List[float],
    fast_check: bool = False,
) -> List:
    ret = []
    # sort files by the id in name (i.e., "../n.py")
    files = sorted(files, key=lambda x: int(x.split("/")[-1].split(".")[0]))
    for file in files:
        code = open(file, "r").read()
        stat, det = untrusted_check(
            code,
            inputs,
            entry_point,
            expected=expected,
            atol=atol,
            ref_time=ref_time,
            fast_check=fast_check,
        )
        ret.append((stat, det))
    return ret


def evaluate_one(problem: dict, r_folder: str, more_eval: bool, iextra=None):
    p_name = problem["task_id"].replace("/", "_")
    atol = problem["atol"]
    code = problem["prompt"] + problem["reference"]
    gen_files = glob.glob(r_folder + f"/{p_name}/*.py")
    entry_point = problem["entry_point"]
    # Get oracle from base questions.
    base_oracle, base_time = trusted_exec(
        code, problem["base_input"], entry_point, record_time=True
    )

    print("Evaluating for {} ...".format(p_name), atol if atol else "")
    rbase = evaluate_files(
        gen_files,
        problem["base_input"],
        base_oracle,
        problem["entry_point"],
        problem["atol"],
        ref_time=base_time,
    )

    base_nsucc = len([r for r in rbase if r[0] == SUCCESS])
    msg = f"{p_name} :: Total {len(gen_files)} :: Base Success {base_nsucc}"

    if more_eval and iextra:
        new_inputs = iextra
        plus_oracle, plus_time = trusted_exec(
            code, iextra, entry_point, record_time=True
        )

        rplus = evaluate_files(
            gen_files,
            new_inputs,
            plus_oracle,
            problem["entry_point"],
            problem["atol"],
            ref_time=plus_time,
        )
        plus_nsucc = len(
            [i for i in range(len(rplus)) if rbase[i][0] == rplus[i][0] == SUCCESS]
        )
        msg += f" :: New Success {plus_nsucc}"

    print(msg)

    return p_name, gen_files, rbase, rplus


def evaluate(flags, problems, extra_inputs=None):
    if flags.parallel is None:
        n_workers = max(1, multiprocessing.cpu_count() // 2)
    else:
        n_workers = flags.parallel

    result_path = os.path.join(flags.r_folder, "eval_results.json")

    if os.path.isfile(result_path) and not flags.i_just_wanna_run:
        print(f"Load from {flags.r_folder + '/eval_results.json'}")
        with open(result_path, "r") as f:
            results = json.load(f)
    else:
        results = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "extra_input_hash": hash(str(problems)),
            "eval": {},
        }

        with ProcessPoolExecutor(max_workers=n_workers) as executor:
            futures = []
            for problem in tqdm(problems):
                p_name = problem["task_id"].replace("/", "_")
                iextra = extra_inputs.get(p_name, None) if extra_inputs else None
                args = (problem, flags.r_folder, flags.more_eval, iextra)
                futures.append(executor.submit(evaluate_one, *args))
            for future in futures:
                p_name, files, rbase, rplus = future.result()
                results["eval"][p_name] = {
                    "files": files,
                    "base": rbase,
                    "plus": rplus,
                }

    if os.path.isfile(result_path) and flags.i_just_wanna_run:
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
    total = np.array([len(r["files"]) for r in results["eval"].values()])
    base_correct = []
    new_correct = []
    for r in results["eval"].values():
        base_correct.append(len([r[0] == SUCCESS for r in r["base"]]))
        new_correct.append(len([r[0] == SUCCESS for r in r["plus"]]))
    base_correct = np.array(base_correct)
    new_correct = np.array(new_correct)
    new_correct = np.logical_and(new_correct, base_correct)

    pass_at_k = {
        f"pass@{k}": estimate_pass_at_k(total, base_correct, k).mean()
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

import itertools
import math
import multiprocessing
import time
from multiprocessing import Array, Value
from typing import Any, Dict, List, Tuple, Union

import numpy as np

from evalplus.data import to_raw
from evalplus.eval.utils import (
    create_tempdir,
    reliability_guard,
    swallow_io,
    time_limit,
)


def compatible_eval_result(results: Dict) -> Dict:
    # compatibility
    for task_results in results["eval"].values():
        # update the "files" field to "nfiles"
        if "files" in task_results and "nfiles" not in task_results:
            task_results["nfiles"] = len(task_results.pop("files"))
    return results


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
def _poly(xs: list, x: float):
    """
    Evaluates polynomial with coefficients xs at point x.
    return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n
    """
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])


SUCCESS = "success"
FAILED = "failed"
TIMEOUT = "timed out"

_SUCCESS = 0
_FAILED = 1
_TIMEOUT = 2
_UNKNOWN = 3

_mapping = {_SUCCESS: SUCCESS, _FAILED: FAILED, _TIMEOUT: TIMEOUT, _UNKNOWN: None}


def is_floats(x) -> bool:
    # check if it is float; List[float]; Tuple[float]
    if isinstance(x, float):
        return True
    if isinstance(x, (list, tuple)):
        return all(isinstance(i, float) for i in x)
    if isinstance(x, np.ndarray):
        return x.dtype == np.float64 or x.dtype == np.float32
    return False


def unsafe_execute(
    entry_point: str,
    code: str,
    inputs,
    expected: List,
    time_limits,
    atol,
    fast_check,
    stat: Value,
    details: Array,
    progress: Value,
):
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
                            assert _poly(*out, inp) <= atol

                        if atol == 0 and is_floats(exp):
                            atol = 1e-6  # enforce atol for float comparison
                        if not exact_match and atol != 0:
                            np.testing.assert_allclose(out, exp, atol=atol)
                        else:
                            assert exact_match
                    except BaseException:
                        if fast_check:
                            raise

                        details[i] = False
                        progress.value += 1
                        continue

                    details[i] = True
                    progress.value += 1
            stat.value = _SUCCESS
        except BaseException:
            stat.value = _FAILED
        # Needed for cleaning up.
        shutil.rmtree = rmtree
        os.rmdir = rmdir
        os.chdir = chdir


def untrusted_check(
    code: str,
    inputs: List[Any],
    entry_point: str,
    expected,
    atol,
    ref_time: List[float],
    fast_check: bool = False,
    min_time_limit: float = 0.1,
    gt_time_limit_factor: float = 2.0,
) -> Tuple[str, np.ndarray]:
    time_limits = [max(min_time_limit, gt_time_limit_factor * t) for t in ref_time]
    timeout = sum(time_limits) + 1
    if not fast_check:
        timeout += 1  # extra time for data collection

    # shared memory objects
    progress = Value("i", 0)
    stat = Value("i", _UNKNOWN)
    details = Array("b", [False for _ in range(len(inputs))])

    p = multiprocessing.Process(
        target=unsafe_execute,
        args=(
            entry_point,
            code,
            inputs,
            expected,
            time_limits,
            atol,
            fast_check,
            # return values
            stat,
            details,
            progress,
        ),
    )
    p.start()
    p.join(timeout=timeout + 1)
    if p.is_alive():
        p.terminate()
        time.sleep(0.1)
    if p.is_alive():
        p.kill()
        time.sleep(0.1)

    stat = _mapping[stat.value]
    details = details[: progress.value]

    if not stat:
        stat = TIMEOUT

    if stat == SUCCESS:
        if len(details) != len(inputs) or not all(details):
            stat = FAILED

    return stat, details


def evaluate_files(
    files: List[str],
    inputs: List,
    expected: List,
    entry_point: str,
    atol: float,
    ref_time: List[float],
    fast_check: bool = False,
    min_time_limit: float = 0.1,
    gt_time_limit_factor: float = 2.0,
) -> List[Tuple[str, List[bool]]]:
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
            min_time_limit=min_time_limit,
            gt_time_limit_factor=gt_time_limit_factor,
        )
        ret.append((stat, det.tolist()))
    return ret

from concurrent.futures import ProcessPoolExecutor
from time import perf_counter
from traceback import format_exc
from typing import Any, Callable, List, Optional

from cirron import Collector

from evalplus.eval.utils import (
    TimeoutException,
    create_tempdir,
    reliability_guard,
    swallow_io,
    time_limit,
)
from evalplus.perf.config import MEMORY_LIMIT_GB, PROFILE_ROUNDS


def are_profiles_broken(profiles) -> bool:
    return not all(isinstance(profile, (float, int)) for profile in profiles)


def physical_runtime_profiler(function, test_inputs) -> float:
    start = perf_counter()
    for test_input in test_inputs:
        function(*test_input)
    return perf_counter() - start


def num_instruction_profiler(function, test_inputs) -> int:
    with Collector() as c:
        for test_input in test_inputs:
            function(*test_input)
    return int(c.counters.instruction_count)


def get_instruction_count(
    profiler: Callable,
    func_code: str,
    entry_point: str,
    test_inputs: List[Any],
    timeout_second_per_test: float,
    memory_bound_gb: int,
    warmup_inputs: Optional[List[Any]],
) -> Optional[float]:

    error = None

    with create_tempdir():
        # These system calls are needed when cleaning up tempdir.
        import os
        import shutil

        rmtree = shutil.rmtree
        rmdir = os.rmdir
        chdir = os.chdir

        # Disable functionalities that can make destructive changes to the test.
        maximum_memory_bytes = memory_bound_gb * 1024 * 1024 * 1024
        reliability_guard(maximum_memory_bytes=maximum_memory_bytes)
        exec_globals = {}

        # run (eval) the func def
        exec(func_code, exec_globals)
        fn = exec_globals[entry_point]

        # warmup the function
        if warmup_inputs:
            for _ in range(3):
                fn(*warmup_inputs)

        compute_cost = None
        try:  # run the function
            with time_limit(timeout_second_per_test):
                with swallow_io():
                    compute_cost = profiler(fn, test_inputs)
        except TimeoutException:
            print("[Warning] Profiling hits TimeoutException")
            error = "TIMEOUT ERROR"
        except MemoryError:
            print("[Warning] Profiling hits MemoryError")
            error = "MEMORY ERROR"
        except:
            print("[CRITICAL] ! Non-time out exception during profiling !")
            error = format_exc()
            print(error)

        # Needed for cleaning up.
        shutil.rmtree = rmtree
        os.rmdir = rmdir
        os.chdir = chdir

    if not error:
        return compute_cost

    return error


def profile(
    func_code: str,
    entry_point: str,
    test_inputs: List[Any],
    timeout_second_per_test: float,
    memory_bound_gb: int = MEMORY_LIMIT_GB,
    profile_rounds: int = PROFILE_ROUNDS,
    profiler: Callable = num_instruction_profiler,
    warmup_inputs: Optional[List[Any]] = None,  # multiple inputs
) -> List[int | float | str]:
    """Profile the func_code against certain input tests.
    The function code is assumed to be correct and if a string is returned, it is an error message.
    """

    def _run():
        with ProcessPoolExecutor(max_workers=1) as executor:
            args = (
                profiler,
                func_code,
                entry_point,
                test_inputs,
                timeout_second_per_test,
                memory_bound_gb,
                warmup_inputs,
            )
            future = executor.submit(get_instruction_count, *args)
            if future.exception():
                print(
                    f"[Profile Error] Exception in profile: {str(future.exception())}..."
                )
                return "UNEXPECTED_ERROR"
            return future.result()

    # setup a process
    return [_run() for _ in range(profile_rounds)]

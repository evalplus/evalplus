import math
import multiprocessing
import time
from typing import Any, List, Union

from evalplus.data import get_human_eval_plus
from evalplus.eval.utils import (
    TimeoutException,
    create_tempdir,
    reliability_guard,
    swallow_io,
    time_limit,
)

MAX_WARMUP_LIMIT = 5
RUN_REPEAT = 25


def execute_for_runtime(
    code: str, inputs: List, warmups: List, entry_point: str
) -> Union[str, float]:
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
            # load functions
            exec_globals = {}
            exec(code, exec_globals)
            fn = exec_globals[entry_point]
            try:
                # warmup calls
                for warmup in warmups:
                    with swallow_io():
                        fn(*warmup)

                start_time = time.time()
                # real call
                with swallow_io():
                    with time_limit(3):
                        fn(*inputs)
                duration = time.time() - start_time

                result.append(duration)
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
    p.join(timeout=3 + 1)
    if p.is_alive():
        p.kill()
    return result[0]


def test_solution_runtime(
    dataset: str = "humaneval",
    task_id: str = "HumanEval/0",
    impl: str = "canonical",
    inputs: Union[str, List[List[Any]]] = "base_input",
):
    if "humaneval" in dataset:
        problems, problem = get_human_eval_plus(), None
        for p in problems:
            if p["task_id"] == task_id:
                problem = p
        assert problem != None, f"invalid {task_id = }"
        entry_point = problem["entry_point"]
        impl = problem["prompt"] + (
            impl if impl != "canonical" else problem["canonical_solution"]
        )
        if inputs == "base_input":
            inputs = problem["base_input"]

        results = [1000, 1000]
        for input_list in inputs:
            # choose warmup input
            warmups = []
            for base_input_list in problem["base_input"]:
                if (
                    hash(str(base_input_list)) != hash(str(input_list))
                    and len(warmups) < MAX_WARMUP_LIMIT
                ):
                    warmups.append(base_input_list)
            runtime_list = [
                execute_for_runtime(impl, input_list, warmups, entry_point)
                for _ in range(RUN_REPEAT)
            ]
            if any(type(x) != float for x in runtime_list):
                print(f"{task_id = } incorrect")
                return None, None

            avg_runtime = sum(runtime_list) / len(runtime_list)
            sd = math.sqrt(
                sum((runtime - avg_runtime) ** 2 for runtime in runtime_list)
                / (RUN_REPEAT - 1)
            )
            if sd < results[1]:
                results[0] = avg_runtime
                results[1] = sd

        return results

import argparse
import multiprocessing
from typing import Dict, List

from fuzz_eval.evaluation.evaluate_helpers import (
    TimeoutException,
    create_tempdir,
    reliability_guard,
    swallow_io,
    time_limit,
)
from fuzz_eval.utils import get_fuzz_eval


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


def evaluate(args, problems):
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

        if args.more_eval:
            # where we would apply the additional testcases.
            raise NotImplementedError("More evaluation has not been implemented")
    pass


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

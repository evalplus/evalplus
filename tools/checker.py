"""This file checks two things:
1. Is the LLMs codegen completed for each benchmark?
2. Warn the code that are not compilable (it could be some impl issues).
"""

import ast
import os
import re
import traceback

from termcolor import colored


def get_all_python_files(folder):
    # return a list of full-path python files
    py_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files


def syntax_check(code, verbose=False):
    try:
        ast.parse(code)
        return True
    except (SyntaxError, MemoryError):
        if verbose:
            traceback.print_exc()
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, required=True)
    parser.add_argument(
        "--dataset", required=True, type=str, choices=["humaneval", "mbpp"]
    )
    parser.add_argument("--nsample", type=int)
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    if args.nsample is None:
        temp = re.findall("temp_(?:\d*\.?\d+)", args.folder)
        if temp and float(temp[0].split("_")[-1]) == 0.0:
            print(colored("Setting nsample = 1 for 0 temp.", "yellow"))
            args.nsample = 1
        else:
            print(colored("Setting nsample = 200 for non-0 temp.", "yellow"))
            args.nsample = 200

    if args.dataset == "humaneval":
        from evalplus.data import get_human_eval_plus

        task_no = [int(x.split("/")[-1]) for x in get_human_eval_plus().keys()]
        dataset_name = "HumanEval"
    elif args.dataset == "mbpp":
        from evalplus.data import get_mbpp_plus

        task_no = [int(x.split("/")[-1]) for x in get_mbpp_plus().keys()]
        dataset_name = "Mbpp"

    ntask = len(task_no)

    print(colored("==============================", "blue"))
    print(colored(" ::: Checking completeness... ", "blue"))
    print(colored(" ::::: All tasks complete?    ", "blue"))
    ndone = 0

    for i in task_no:
        task_folder = os.path.join(args.folder, f"{dataset_name}_{i}")
        if not os.path.exists(task_folder):
            print(colored(f" ⚠️ {dataset_name}_{i} is missing!", "red"))
            continue
        # get the # of .py files under task_folder
        nfiles = len(get_all_python_files(task_folder))
        if nfiles != args.nsample:
            print(
                colored(
                    f" ⚠️ {dataset_name}_{i} only has {nfiles} samples! But {args.nsample} are expected.",
                    "red",
                )
            )
            continue
        ndone += 1
    if ntask != ndone:
        ntbd = ntask - ndone
        print(colored(f" ::::: ⚠️ {ntbd}/{ntask} tasks incomplete!", "red"))
    else:
        print(colored(f" ::::: All {ntask} tasks complete!", "green"))

    print(colored("==============================", "blue"))
    print(colored(" ::: Checking compilation...  ", "blue"))
    print(colored(" ::::: All code compilable?   ", "blue"))
    ncode = 0
    nwrong = 0
    for i in task_no:
        task_folder = os.path.join(args.folder, f"{dataset_name}_{i}")
        # folder must exist
        if not os.path.exists(task_folder):
            continue

        for pyf in get_all_python_files(task_folder):
            ncode += 1
            code = open(pyf).read()
            if code.strip() == "":
                print(colored(f" ⚠️ {pyf} is empty!", "red"))
                nwrong += 1
            elif not syntax_check(code, args.verbose):
                print(colored(f" ⚠️ {pyf} is not compilable!", "red"))
                nwrong += 1
    if ncode != nwrong:
        print(colored(f" ::::: ⚠️ {nwrong}/{ncode} code are not compilable!", "red"))

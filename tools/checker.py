"""This file checks two things:
1. Is the LLMs codegen completed for each benchmark?
2. Warn the code that are not compilable (it could be some impl issues).
"""

from termcolor import colored

from evalplus.data import load_solutions
from evalplus.sanitize import syntax_check

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=str, required=True)
    parser.add_argument(
        "--dataset", required=True, type=str, choices=["humaneval", "mbpp"]
    )
    parser.add_argument("--nsample", type=int, default=1)
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    # List[Dict{"task_id", "solution"}]
    solutions = load_solutions(args.samples)

    if args.dataset == "humaneval":
        from evalplus.data import get_human_eval_plus

        dataset = get_human_eval_plus()
        dataset_name = "HumanEval"
    elif args.dataset == "mbpp":
        from evalplus.data import get_mbpp_plus

        dataset = get_mbpp_plus()
        dataset_name = "Mbpp"

    id2solutions = {}
    for solution in solutions:
        task_id = solution["task_id"]
        if task_id not in id2solutions:
            id2solutions[task_id] = []
        if "solution" not in solution:
            assert "completion" in solution, "solution or completion must exist!"
            solution["solution"] = dataset[task_id]["prompt"] + solution["completion"]
        id2solutions[task_id].append(solution)

    nsample = max(args.nsample, max(len(v) for v in id2solutions.values()))
    print(colored("==============================", "blue"))
    print(colored(" ::: Checking completeness... ", "blue"))
    print(colored(" ::::: All tasks complete?    ", "blue"))
    ndone = 0

    task_ids = dataset.keys()
    ntask = len(task_ids)
    for task_id in task_ids:
        if task_id not in id2solutions:
            print(colored(f" ⚠️ {task_id} is missing!", "red"))
            continue
        nfiles = len(id2solutions[task_id])
        if nfiles == nsample:
            ndone += 1
            continue

        print(
            colored(
                f" ⚠️ {task_id} only has {nfiles} samples! But {nsample} are expected.",
                "red",
            )
        )

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
    for task_id in task_ids:
        # task_id must exist
        if task_id not in id2solutions:
            continue

        for solution in id2solutions[task_id]:
            ncode += 1
            code = solution["solution"]
            dbg_identifier = solution["_identifier"]
            if code.strip() == "":
                print(colored(f" ⚠️ {dbg_identifier} is empty!", "red"))
                nwrong += 1
            elif not syntax_check(code, args.verbose):
                print(colored(f" ⚠️ {dbg_identifier} is not compilable!", "red"))
                nwrong += 1
    if 0 != nwrong:
        print(colored(f" ::::: ⚠️ {nwrong}/{ncode} code are not compilable!", "red"))
    else:
        print(colored(f" ::::: All {ncode} code are compilable!", "green"))

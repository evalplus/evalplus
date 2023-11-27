import argparse
import json
import os
from typing import Any, Dict, List

from rich.progress import track

from evalplus.eval.utils import swallow_io
from evalplus.evaluate import evaluate
from tools.tsr.utils import (
    clean,
    execute_cmd,
    get_cmd_output,
    get_problems,
    get_task_ids,
    to_path,
)


def prepare_mutants(mutation_dir: str, dataset: str):
    pwd = os.getcwd()
    task_ids = get_task_ids(dataset)
    problems = get_problems(dataset)
    os.makedirs(mutation_dir, exist_ok=True)
    for task_id in track(task_ids, "Generating mutants"):
        task_dir = os.path.join(mutation_dir, to_path(task_id))
        os.makedirs(task_dir, exist_ok=True)
        if any(map(lambda filename: filename.startswith("m"), os.listdir(task_dir))):
            # already have mutants
            continue
        # Make groundtruth
        groundtruth_code = (
            problems[task_id]["prompt"] + problems[task_id]["canonical_solution"]
        )
        with open(os.path.join(task_dir, "gt.py"), "w") as f:
            f.write(groundtruth_code)
        # Make dummy pytest
        with open(os.path.join(task_dir, "test_dummy.py"), "w") as f:
            f.write("def test_dummy():\n    pass")
        # Use mutmut to generate mutants
        os.chdir(task_dir)
        clean(".mutmut-cache")
        execute_cmd(["mutmut run", "--paths-to-mutate=gt.py", "1>/dev/null"])
        try:
            # Collect metainfo
            total_mutants = int(
                get_cmd_output(["mutmut", "results"]).split("\n")[-2].split("-")[-1]
            )
        except:
            total_mutants = 0
        # Dump mutants
        for i in range(1, total_mutants + 1):
            execute_cmd(["cp", "gt.py", "gt_copy.py"])
            execute_cmd(["mutmut", "apply", str(i)])
            execute_cmd(["mv", "gt.py", f"m{i}.py"])
            execute_cmd(["mv", "gt_copy.py", "gt.py"])
        # Remove gt and dummy pytest
        execute_cmd(["rm", "gt.py"])
        execute_cmd(["rm", "test_dummy.py"])
        clean(".mutmut-cache")
        os.chdir(pwd)


def mutants_eval(mutation_dir: str, dataset: str):
    args = argparse.Namespace(
        dataset=dataset,
        samples=mutation_dir,
        base_only=False,
        parallel=None,
        i_just_wanna_run=False,
        test_details=True,
        min_time_limit=0.2,
        gt_time_limit_factor=4.0,
        mini=False,
    )
    print("Evaluating mutants... ", end="", flush=True)
    with swallow_io():
        evaluate(args)
    print("Done")


def collect_mutation_info(
    eval_path: str, dataset: str
) -> Dict[str, Dict[str, List[Any]]]:
    mutation_info = {task_id: {} for task_id in get_task_ids(dataset)}
    assert os.path.isfile(
        eval_path
    ), f"mutation testing result file {eval_path} missing!"
    eval_res = json.load(open(eval_path, "r"))["eval"]
    for task_id, v in eval_res.items():
        for i_code, (status, res_list) in enumerate(v["plus"]):
            if status == "success":
                continue
            for i_test, res in enumerate(res_list):
                test_id = f"plus_{i_test}"
                if res == False:
                    mutation_info[task_id].setdefault(test_id, []).append(
                        ("mutant", i_code)
                    )
    return mutation_info


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, choices=["humaneval", "mbpp"])
    parser.add_argument("--report_dir", required=True, type=str)
    args = parser.parse_args()

    mutation_dir = os.path.join(args.report_dir, "mutation_cache")
    prepare_mutants(mutation_dir, args.dataset)
    mutants_eval(mutation_dir, args.dataset)
    collect_mutation_info(os.path.join(mutation_dir, "eval_results.json"), args.dataset)

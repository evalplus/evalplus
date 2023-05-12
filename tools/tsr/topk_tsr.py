import argparse
import json
import os
import random
from collections import defaultdict
from typing import Any, Dict, List

from rich.progress import track

from evalplus.data import get_human_eval_plus
from evalplus.evaluate import evaluate_humaneval

LLM_HOME_PATH = "/JawTitan/yuyao-data/humaneval"
model_paths = os.listdir(LLM_HOME_PATH)
HUMANEVAL_COUNT = 164

problems = get_human_eval_plus()
new_problems = {}

models = [
    "codegen-2b",
    "codegen-6b",
    "codegen-16b",
    "codegen2-1b",
    "codegen2-3b",
    "codegen2-7b",
    "codegen2-16b",
    "vicuna-7b",
    "vicuna-13b",
    "stablelm-7b",
    "incoder-1b",
    "incoder-6b",
    "polycoder",
    "chatgpt",
    "santacoder",
    "starcoder",
    "gptneo-2b",
    "gpt-4",
    "gpt-j",
]
pass_at_k = {
    "codegen-2b": 20.7,
    "codegen-6b": 25.6,
    "codegen-16b": 26.8,
    "codegen2-1b": 9.1,
    "codegen2-3b": 12.8,
    "codegen2-7b": 16.5,
    "codegen2-16b": 16.5,
    "vicuna-7b": 10.4,
    "vicuna-13b": 15.2,
    "stablelm-7b": 2.4,
    "incoder-1b": 10.4,
    "incoder-6b": 12.2,
    "polycoder": 5.5,
    "chatgpt": 63.4,
    "santacoder": 12.8,
    "starcoder": 29.3,
    "gptneo-2b": 6.7,
    "gpt-4": 76.2,
    "gpt-j": 10.4,
}
temps = ["0.0", "0.2", "0.4", "0.6", "0.8"]
cover_info = {f"HumanEval/{i}": {} for i in range(HUMANEVAL_COUNT)}
"""
cover_info dictionary structure:
task_id (e.g. HumanEval_{x}):
    test_id (e.g., plus_{x}):
        a list, each element is a tuple (X, Y), where
        * X \in {"mutant"(mutation testing), model_name(sample killing), branch_name(coverage)}
        * Y \in {code_id(mutation testing, sample killing), "gt"(coverage)}
"""


def compute_score(model_path: str):
    for model in models:
        if model in model_path:
            return pass_at_k[model]
    return 0


def add_kill_info():
    kill_info = {f"HumanEval/{i}": {} for i in range(HUMANEVAL_COUNT)}
    for model_path in track(model_paths, description="Collecting sets..."):
        if not model_path[-1].isdigit():
            continue
        eval_json_path = os.path.join(LLM_HOME_PATH, model_path, "base_info.json")
        if not os.path.exists(eval_json_path):
            os.system(
                f'mv {eval_json_path.replace("base_info", "eval_results")} {eval_json_path}'
            )
        with open(eval_json_path, "r") as f:
            res = json.load(f)["eval"]
            for task_id, v in res.items():
                for i_code, (status, res_list) in enumerate(v["plus"]):
                    if status == "success":
                        continue
                    for i_test, res in enumerate(res_list):
                        test_id = f"plus_{i_test}"
                        if res == False:
                            cover_info[task_id].setdefault(test_id, []).append(
                                (model_path, i_code)
                            )
                            kill_info[task_id].setdefault(test_id, []).append(
                                (model_path, i_code)
                            )
    return kill_info


def add_mutation_info():
    eval_json_path = os.path.join(LLM_HOME_PATH, "mutants", "eval_results.json")
    mutation_info = {f"HumanEval/{i}": {} for i in range(HUMANEVAL_COUNT)}
    with open(eval_json_path, "r") as f:
        res = json.load(f)["eval"]
        for task_id, v in res.items():
            for i_code, (status, res_list) in enumerate(v["plus"]):
                if status == "success":
                    continue
                for i_test, res in enumerate(res_list):
                    test_id = f"plus_{i_test}"
                    if res == False:
                        cover_info[task_id].setdefault(test_id, []).append(
                            ("mutant", i_code)
                        )
                        mutation_info[task_id].setdefault(test_id, []).append(
                            ("mutant", i_code)
                        )
    return mutation_info


def add_coverage_info():
    COVERAGE = os.path.join(LLM_HOME_PATH, "coverage_info")
    coverage_info = {f"HumanEval/{i}": {} for i in range(HUMANEVAL_COUNT)}
    for i in range(HUMANEVAL_COUNT):
        task_id = f"HumanEval/{i}"
        with open(os.path.join(COVERAGE, f"{i}.json"), "r") as f:
            cov_dict = json.load(f)
        for test_id, branch_cover in cov_dict.items():
            cover_info[task_id].setdefault(test_id, []).extend(
                [(br, "gt") for br in branch_cover]
            )
            coverage_info[task_id].setdefault(test_id, []).extend(
                [(br, "gt") for br in branch_cover]
            )
    return coverage_info


def get_score_info(exclude: str):
    score_info = {f"HumanEval/{i}": {} for i in range(HUMANEVAL_COUNT)}
    for task_id, tests in cover_info.items():
        for test_id, cover_list in tests.items():
            score_info[task_id][test_id] = {"coverage": 0, "sample": 0, "mutation": 0}
            for identifier, _ in cover_list:
                if identifier.startswith("mutant"):
                    score_info[task_id][test_id]["mutation"] += 1
                elif identifier.startswith("BR"):
                    score_info[task_id][test_id]["coverage"] += 1
                else:
                    if exclude not in identifier:
                        score_info[task_id][test_id]["sample"] += compute_score(
                            identifier
                        )
    return score_info


def compute_avg_test(problem: Dict[str, Dict[str, Any]]):
    sum_tests = sum(
        len(info["base_input"]) + len(info["plus_input"]) for info in problem.values()
    )
    return sum_tests / len(problem)


def initialization():
    for i in range(HUMANEVAL_COUNT):
        task_id = f"HumanEval/{i}"
        otask = problems[task_id]
        task = {
            "task_id": task_id,
            "prompt": otask["prompt"],
            "contract": otask["contract"],
            "canonical_solution": otask["canonical_solution"],
            "entry_point": otask["entry_point"],
            "base_input": otask["base_input"],
            "plus_input": [],
            "atol": otask["atol"],
        }
        new_problems[task_id] = task


def greedy_cover(info_dict, flags):
    for i in range(HUMANEVAL_COUNT):
        task_id = f"HumanEval/{i}"
        tests = info_dict[task_id]
        q, U = [], set()
        for test_name, test_cover in tests.items():
            cover_set = set()
            for model_path, i_code in test_cover:
                # For LLM sample killing info, filter out elements in the test set
                if flags.model not in model_path:
                    cover_set.add((model_path, i_code))
            q.append((test_name, cover_set))
            U = U.union(cover_set)
        # Greedy algorithm for min set cover
        min_cover = []
        while len(U) > 0:
            max_uncover_set, max_test_name = {}, ""
            for test_name, cover_set in q:
                if len(cover_set) > len(max_uncover_set):
                    max_uncover_set = cover_set
                    max_test_name = test_name
            min_cover.append(max_test_name)
            U = U - max_uncover_set
            qq = []
            for test_name, cover_set in q:
                new_cover_set = U.intersection(cover_set)
                if len(new_cover_set) != 0:
                    qq.append((test_name, new_cover_set))
            q = qq
        for test_id in min_cover:
            if test_id.startswith("plus"):
                if test_id not in new_problems[task_id]["plus_input"]:
                    new_problems[task_id]["plus_input"].append(test_id)


def min_set_cover(flags):
    disable_sample = flags.stage == "s1" and flags.disable_sample
    disable_coverage = flags.stage == "s1" and flags.disable_coverage
    disable_mutation = flags.stage == "s1" and flags.disable_mutation
    if not disable_sample:
        info_dict = add_kill_info()
        greedy_cover(info_dict, flags)
    if not disable_coverage:
        info_dict = add_coverage_info()
        greedy_cover(info_dict, flags)
    if not disable_mutation:
        info_dict = add_mutation_info()
        greedy_cover(info_dict, flags)


def topk_selection(flags):
    disable_sample = flags.stage == "s2" and flags.disable_sample
    disable_coverage = flags.stage == "s2" and flags.disable_coverage
    disable_mutation = flags.stage == "s2" and flags.disable_mutation

    score_info = get_score_info(flags.model)
    for i in range(HUMANEVAL_COUNT):
        task_id = f"HumanEval/{i}"
        lists = []
        if not disable_sample:
            lists.append(
                sorted(
                    list(score_info[task_id].keys()),
                    key=lambda x: score_info[task_id][x]["sample"],
                    reverse=True,
                )
            )
        if not disable_coverage:
            lists.append(
                sorted(
                    list(score_info[task_id].keys()),
                    key=lambda x: score_info[task_id][x]["coverage"],
                    reverse=True,
                )
            )
        if not disable_mutation:
            lists.append(
                sorted(
                    list(score_info[task_id].keys()),
                    key=lambda x: score_info[task_id][x]["mutation"],
                    reverse=True,
                )
            )
        metric_count, pc, remaining = len(lists), 0, flags.K
        while remaining > 0 and any(len(l) != 0 for l in lists):
            if len(lists[pc]) == 0:
                pc = (pc + 1) % metric_count
                continue
            test_id = lists[pc][0]
            lists[pc] = lists[pc][1:]
            if test_id not in new_problems[task_id]["plus_input"]:
                new_problems[task_id]["plus_input"].append(test_id)
                remaining -= 1


def export_report(flags):
    for num in range(HUMANEVAL_COUNT):
        task_id = f"HumanEval/{num}"
        for i, test_id in enumerate(new_problems[task_id]["plus_input"]):
            index = int(test_id.split("_")[-1])
            new_problems[task_id]["plus_input"][i] = problems[task_id]["plus_input"][
                index
            ]

    args = argparse.Namespace(
        dataset="humaneval",
        samples=f"{LLM_HOME_PATH}/{flags.model}_temp_0.0",
        parallel=32,
        base_only=False,
        i_just_wanna_run=True,
        full=False,
    )
    exec_time, pass_at_k_dict = evaluate_humaneval(args, new_problems)
    tsr_dict = {
        "ntests": compute_avg_test(new_problems),
        "pass@1": pass_at_k_dict["pass@1"],
        "runtime": exec_time,
    }
    suffix = "full"
    if flags.disable_coverage:
        suffix = "coverage"
    if flags.disable_mutation:
        suffix = "mutation"
    if flags.disable_sample:
        suffix = "sample"
    with open(
        os.path.join(LLM_HOME_PATH, f"{flags.model}_{flags.stage}_{suffix}.json"), "w"
    ) as f:
        json.dump(tsr_dict, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=models)
    parser.add_argument("--disable_coverage", action="store_true", default=False)
    parser.add_argument("--disable_mutation", action="store_true", default=False)
    parser.add_argument("--disable_sample", action="store_true", default=False)
    parser.add_argument("--stage", choices=["s1", "s2"], default="s2")
    parser.add_argument("--K", type=int, default=50)
    parser.add_argument(
        "--strategy", default="heuristics", choices=["heuristics", "random"]
    )
    args = parser.parse_args()

    initialization()

    min_set_cover(args)
    if args.stage == "s2":
        topk_selection(args)

    # export_report(args)

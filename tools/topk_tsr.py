import argparse
import json
import os
from collections import defaultdict
from typing import Any, Dict, List

from rich.progress import track

from evalplus.data import get_human_eval_plus
from evalplus.evaluate import evaluate

LLM_HOME_PATH = "/JawTitan/yuyao-data/humaneval"
K = 5
model_paths = os.listdir(LLM_HOME_PATH)

problems = get_human_eval_plus()

models = [
    "codegen-2b",
    "codegen-6b",
    "codegen-16b",
    "vicuna-7b",
    "vicuna-13b",
    "stablelm-7b",
    "incoder-1b",
    "incoder-6b",
    "polycoder",
    "chatgpt",
    "santacoder",
    "gptneo-2b",
    "gpt-4",
    "gpt-j",
]
pass_at_k = {
    "codegen-2b": 20.7,
    "codegen-6b": 25.6,
    "codegen-16b": 26.8,
    "vicuna-7b": 10.4,
    "vicuna-13b": 15.2,
    "stablelm-7b": 2.4,
    "incoder-1b": 10.4,
    "incoder-6b": 12.2,
    "polycoder": 5.5,
    "chatgpt": 63.4,
    "santacoder": 12.8,
    "gptneo-2b": 6.7,
    "gpt-4": 76.2,
    "gpt-j": 10.4,
}
temps = ["0.0", "0.2", "0.4", "0.6", "0.8"]


def compute_score(model_path: str):
    for model in models:
        if model in model_path:
            return pass_at_k[model]
    return 0


def get_cover_info():
    cover_info = {f"HumanEval/{i}": {} for i in range(164)}
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
                for i_code, (status, res_list) in enumerate(v["base"]):
                    if status == "success":
                        continue
                    for i_test, res in enumerate(res_list):
                        test_id = f"base_{i_test}"
                        if res == False:
                            cover_info[task_id].setdefault(test_id, []).append(
                                (model_path, i_code)
                            )
                for i_code, (status, res_list) in enumerate(v["plus"]):
                    if status == "success":
                        continue
                    for i_test, res in enumerate(res_list):
                        test_id = f"plus_{i_test}"
                        if res == False:
                            cover_info[task_id].setdefault(test_id, []).append(
                                (model_path, i_code)
                            )
    return cover_info


def get_score_info(cover_info: Dict[str, Dict[str, List[Any]]], exclude: str):
    score_info = {f"HumanEval/{i}": defaultdict(int) for i in range(164)}
    for task_id, tests in cover_info.items():
        score = 0
        for test_id, kills in tests.items():
            for model_path, _ in kills:
                if exclude not in model_path:
                    score += compute_score(model_path)
            score_info[task_id][test_id] = score
    return score_info


def compute_avg_test(problem: Dict[str, Dict[str, Any]]):
    sum_tests = sum(
        len(info["base_input"]) + len(info["plus_input"]) for info in problem.values()
    )
    return sum_tests / len(problem)


cover_info = get_cover_info()

for model in models:
    if "gpt-4" not in model:
        continue
    score_info = get_score_info(cover_info, model)
    new_problems = {}
    for i in range(164):
        task_id = f"HumanEval/{i}"
        otask = problems[task_id]
        task = {
            "task_id": task_id,
            "prompt": otask["prompt"],
            "contract": otask["contract"],
            "canonical_solution": otask["canonical_solution"],
            "entry_point": otask["entry_point"],
            "base_input": [],
            "plus_input": [],
            "atol": otask["atol"],
        }
        new_problems[task_id] = task
    for i in track(range(164), "min set cover"):
        task_id = f"HumanEval/{i}"
        tests = cover_info[task_id]
        q, U = [], set()
        for test_name, test_cover in tests.items():
            cover_set = set()
            for model_path, i_code in test_cover:
                # if True:
                if model not in model_path:
                    cover_set.add((model_path, i_code))
            q.append((test_name, cover_set))
            U = U.union(cover_set)
        # Greedy
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
                index = int(test_id.split("_")[-1])
                inputs = problems[task_id]["plus_input"][index]
                new_problems[task_id]["plus_input"].append(inputs)
    for task_id, tests in score_info.items():
        num = K * len(problems[task_id]["base_input"]) - len(
            new_problems[task_id]["plus_input"]
        )
        if num <= 0:
            continue
        for test_id in sorted(tests, key=lambda x: -tests[x])[
            : K * len(problems[task_id]["base_input"])
        ]:
            index = int(test_id.split("_")[-1])
            if test_id.startswith("base"):
                inputs = problems[task_id]["base_input"][index]
                new_problems[task_id]["base_input"].append(inputs)
            else:
                inputs = problems[task_id]["plus_input"][index]
                if inputs not in new_problems[task_id]["plus_input"]:
                    new_problems[task_id]["plus_input"].append(inputs)
        new_problems[task_id]["base_input"] = problems[task_id]["base_input"]
    args = argparse.Namespace(
        dataset="humaneval",
        samples=f"{LLM_HOME_PATH}/{model}_temp_0.0",
        parallel=32,
        base_only=False,
        i_just_wanna_run=True,
        full=True,
    )
    exec_time, pass_at_k_dict = evaluate(args, new_problems)
    o_exec_time, o_pass_at_k_dict = evaluate(args, problems)
    tsr_dict = {
        "ntests": compute_avg_test(new_problems),
        "pass@1_before": o_pass_at_k_dict["pass@1"],
        "pass@1_after": pass_at_k_dict["pass@1"],
        "runtime_before": o_exec_time,
        "runtime_after": exec_time,
    }
    with open(os.path.join(LLM_HOME_PATH, f"{model}.json"), "w") as f:
        json.dump(tsr_dict, f, indent=4)

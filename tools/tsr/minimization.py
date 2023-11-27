import argparse
import json
import os
import pickle
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple

from rich.progress import track

from evalplus.data import write_jsonl
from tools.tsr.coverage_init import collect_coverage_info
from tools.tsr.mutation_init import collect_mutation_info
from tools.tsr.sample_init import collect_sample_info
from tools.tsr.utils import get_problems, get_task_ids, to_path


def global_util_init(dataset: str):
    global problems
    global task_ids
    global problem_count
    problems = get_problems(dataset)
    task_ids = get_task_ids(dataset)
    problem_count = len(problems)


###########################
# Greedy Min Set Covering #
###########################


def merge_set_cover(*args) -> Dict[str, List[str]]:
    merged_set_cover = {task_id: [] for task_id in task_ids}
    for set_cover_dict in args:
        for task_id, plus_tests in set_cover_dict.items():
            for plus_test in plus_tests:
                if plus_test not in merged_set_cover[task_id]:
                    merged_set_cover[task_id].append(plus_test)
    return merged_set_cover


def greedy_cover(
    task_id: str, tests: Dict[str, List[Any]], exclude_model: str
) -> Tuple[str, List[str]]:
    q, U = [], set()
    for test_name, test_cover in tests.items():
        cover_set = set()
        for model_path, i_code in test_cover:
            if exclude_model not in model_path:
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
    return task_id, min_cover


def parallel_greedy_cover(
    info_dict: Optional[Dict[str, Dict[str, List[Any]]]],
    exclude_model: str,
    type: str,
    **kwargs,
) -> Dict[str, List[str]]:
    plus_tests = {task_id: [] for task_id in task_ids}

    with ProcessPoolExecutor(max_workers=32) as executor:
        futures = []
        for task_id in task_ids:
            if type == "sample":
                path_task_id = to_path(task_id)
                sample_dir = kwargs["sample_dir"]
                with open(os.path.join(sample_dir, f"{path_task_id}.pkl"), "rb") as f:
                    td = pickle.load(f)
                args = (task_id, td, exclude_model)
            else:
                args = (task_id, info_dict[task_id], exclude_model)
            futures.append(executor.submit(greedy_cover, *args))
        for future in track(as_completed(futures), f"min set cover :: {type}"):
            task_id, min_cover = future.result()
            plus_tests[task_id] = min_cover

    return plus_tests


#####################
# Collect Set Cover #
#####################


def get_coverage_set_cover(
    coverage_dir: str, exclude_model: str, dataset: str
) -> Dict[str, List[str]]:
    coverage_info_dict = collect_coverage_info(coverage_dir, dataset)
    return parallel_greedy_cover(coverage_info_dict, exclude_model, "coverage")


def get_mutation_set_cover(
    mutation_dir: str, exclude_model: str, dataset: str
) -> Dict[str, List[str]]:
    mutation_info_dict = collect_mutation_info(
        os.path.join(mutation_dir, "eval_results.json"), dataset
    )
    return parallel_greedy_cover(mutation_info_dict, exclude_model, "mutation")


def get_sample_set_cover(
    sample_dir: str, sample_eval_dir: str, exclude_model: str, dataset: str
) -> Dict[str, List[str]]:
    collect_sample_info(sample_dir, sample_eval_dir, dataset)
    return parallel_greedy_cover(None, exclude_model, "sample", sample_dir=sample_dir)


#################
# pass@1 greedy #
#################


def compute_avg_test(set_cover_info: Dict[str, List[str]]) -> float:
    sum_tests = sum(
        len(problems[task_id]["base_input"]) + len(set_cover_info[task_id])
        for task_id in task_ids
    )
    return sum_tests / problem_count


def gen_report(set_cover_info: Dict[str, List[str]], sample_eval_dir: str, model: str):
    tsr_dict = {"ntests": compute_avg_test(set_cover_info), "pass@1": 0}
    model_path = os.path.join(sample_eval_dir, f"{model}_temp_0.0", "eval_results.json")
    with open(model_path, "r") as f:
        mdict = json.load(f)
    correct_cnt = 0
    for task_id in task_ids:
        legacy_task_id = task_id
        if legacy_task_id not in mdict["eval"]:
            legacy_task_id = legacy_task_id.replace("/", "_")
        if mdict["eval"][legacy_task_id]["base"][0][0] != "success":
            continue
        correct = True
        for plus_id in set_cover_info[task_id]:
            index = int(plus_id.split("_")[-1])
            if mdict["eval"][legacy_task_id]["plus"][0][1][index] == False:
                correct = False
                break
        if correct:
            correct_cnt += 1
    tsr_dict["pass@1"] = correct_cnt / problem_count
    return tsr_dict


def dump_humaneval_plus_mini(set_cover_info: Dict[str, List[str]], mini_path: str):
    new_problems = []
    for task_id in task_ids:
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
        for plus_test in set_cover_info[task_id]:
            index = int(plus_test.split("_")[-1])
            task["plus_input"].append(otask["plus_input"][index])
        new_problems.append(deepcopy(task))
    write_jsonl(os.path.join(mini_path, "HumanEvalPlus-Mini.jsonl"), new_problems)


def main(flags):
    coverage_dir = os.path.join(flags.report_dir, "coverage_cache")
    mutation_dir = os.path.join(flags.report_dir, "mutation_cache")
    sample_dir = os.path.join(flags.report_dir, "sample_cache")
    os.makedirs(flags.report_dir, exist_ok=True)

    exclude_model: str = flags.model
    if exclude_model.endswith("b"):  # format: model_name + parameter size
        exclude_model = "".join(exclude_model.split("-")[:-1])

    coverage_set_cover = get_coverage_set_cover(
        coverage_dir, exclude_model, flags.dataset
    )
    mutation_set_cover = get_mutation_set_cover(
        mutation_dir, exclude_model, flags.dataset
    )
    sample_set_cover = get_sample_set_cover(
        sample_dir, flags.sample_eval_dir, exclude_model, flags.dataset
    )
    merged_set_cover = merge_set_cover(
        coverage_set_cover, mutation_set_cover, sample_set_cover
    )

    if flags.model != "ALL":
        final_report = dict()
        # Stage 1: Coverage min set cover
        final_report["coverage"] = gen_report(
            coverage_set_cover, flags.sample_eval_dir, flags.model
        )
        # Stage 2: Mutation min set cover
        final_report["mutation"] = gen_report(
            mutation_set_cover, flags.sample_eval_dir, flags.model
        )
        # Stage 3: Sampling min set cover
        final_report["sample"] = gen_report(
            sample_set_cover, flags.sample_eval_dir, flags.model
        )
        # Stage 4: All
        final_report["full"] = gen_report(
            merged_set_cover, flags.sample_eval_dir, flags.model
        )
        with open(
            os.path.join(flags.report_dir, f"report_{flags.model}.json"), "w"
        ) as f:
            json.dump(final_report, f, indent=4)
    else:
        dump_humaneval_plus_mini(merged_set_cover, flags.mini_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, type=str, help="Model for testing")
    parser.add_argument("--dataset", type=str, choices=["humaneval", "mbpp"])
    parser.add_argument(
        "--report_dir", type=str, help="Path to JSON report and cache files"
    )
    parser.add_argument(
        "--sample_eval_dir", type=str, help="Path to sample evaluation files"
    )
    parser.add_argument("--mini_path", type=str, help="Path to Mini Dataset")
    args = parser.parse_args()

    global_util_init(args.dataset)
    main(args)

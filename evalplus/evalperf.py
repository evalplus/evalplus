"""Compute the Differential Performance Scores (DPS) and DPS_{norm} of given samples from a model.

Check our COLM paper for more details: https://www.arxiv.org/abs/2408.06450

^Updates from the COLM paper:
* Condition to activate efficiency evaluation for a task:
  * Paper: as long as you have at least one correct solution, and we select up to 10 correct solutions for efficiency sampling
  * Here: you need to have at least `min_correct` correct solutions, and we evaluate the efficiency of all correct solutions
  * Updating rationale: to make the evaluation more statistically robust

@inproceedings{liu2024evaluating,
  title = {Evaluating Language Models for Efficient Code Generation},
  author = {Liu, Jiawei and Xie, Songrun and Wang, Junhao and Wei, Yuxiang and Ding, Yifeng and Zhang, Lingming},
  booktitle = {First Conference on Language Modeling},
  year = {2024},
  url = {https://openreview.net/forum?id=IBCBMeAhmC},
}
"""

import json
import multiprocessing
import os
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from statistics import mean
from typing import Dict, List, Optional, Tuple

import rich
from rich.syntax import Syntax
from rich.table import Table

from evalplus.codegen import run_codegen
from evalplus.data import (
    get_evalperf_data,
    get_human_eval_plus,
    get_human_eval_plus_hash,
    get_mbpp_plus,
    get_mbpp_plus_hash,
)
from evalplus.data.mbpp import mbpp_deserialize_inputs
from evalplus.data.utils import stream_jsonl
from evalplus.eval import PASS, untrusted_check
from evalplus.eval._special_oracle import MBPP_OUTPUT_NOT_NONE_TASKS
from evalplus.evaluate import get_groundtruth
from evalplus.perf.config import EVALUATION_TIMEOUT_SECOND_PER_TEST
from evalplus.perf.profile import are_profiles_broken, profile, simple_test_profiler
from evalplus.utils import progress

_REFERENCE_EXEC_TIMES = 3


def correctness_check(
    solution: str, dataset: str, task: Dict, expected_output: List
) -> Tuple:
    assert isinstance(solution, str)
    result = untrusted_check(
        dataset,
        solution,
        task["base_input"] + list(task["plus_input"]),
        task["entry_point"],
        expected_output["base"] + expected_output["plus"],
        task["atol"],
        expected_output["base_time"] + expected_output["plus_time"],
        fast_check=True,
        min_time_limit=EVALUATION_TIMEOUT_SECOND_PER_TEST,
        gt_time_limit_factor=4.0,
    )
    return result, solution


def get_evalplus_data():
    problems_he = get_human_eval_plus(noextreme=True)
    dataset_hash = get_human_eval_plus_hash(noextreme=True)
    expected_output_human = get_groundtruth(problems_he, dataset_hash, [])
    problems_mbpp = get_mbpp_plus(noextreme=True)
    dataset_hash = get_mbpp_plus_hash(noextreme=True)
    expected_output_mbpp = get_groundtruth(
        problems_mbpp,
        dataset_hash,
        MBPP_OUTPUT_NOT_NONE_TASKS,
    )
    problems = {**problems_he, **problems_mbpp}
    expected_output = {**expected_output_human, **expected_output_mbpp}
    return problems, expected_output


def summarize_evalperf(eval_results: Dict):
    # print a rich table
    dps = mean([res["dps"] for res in eval_results.values() if res["dps"] is not None])
    dps_norm = mean(
        [
            res["dps_norm"]
            for res in eval_results.values()
            if res["dps_norm"] is not None
        ]
    )
    pass_1 = mean(
        [res["pass@1"] for res in eval_results.values() if res["pass@1"] is not None]
    )
    n_evalperfed = len([res for res in eval_results.values() if res["dps"] is not None])

    table = Table(
        title="EvalPerf Summary",
        show_header=True,
        header_style="bold",
    )
    table.add_column("DPS", style="dim")
    table.add_column("DPS_norm", style="dim")
    table.add_column("Pass@1", style="dim")
    table.add_column("#EvalPerf-ed tasks", style="dim")

    table.add_row(f"{dps:.1f}", f"{dps_norm:.1f}", f"{pass_1:.1f}%", n_evalperfed)

    rich.print(table)


def worker_on_one_task(
    task_id: str,
    ptask: Dict,  # EvalPerf data
    samples: list,
    ctask: Dict,  # EvalPlus data
    expected_output: Dict,
    min_correct: int,
    n_workers: int,
    lazy_evaluation: bool,
):
    assert isinstance(
        samples, list
    ), f"{task_id}: samples is not a list but {type(samples)}"
    rich.print(f"Start processing: {task_id}")

    ######################### Meta information #########################
    n_reference = len(ptask["reference"])
    entry_point = ptask["entry_point"]
    ####################################################################

    ret_dict = {
        "task_id": task_id,
        "results": [],
        "ref": [
            {"solution": s, "score": r, "_num_cpu_instructions": None}
            for s, r in zip(ptask["reference"], ptask["scores"])
        ],
        "dps": None,
        "dps_norm": None,
        "pass@1": None,
    }

    # Correctness checking
    n_passing = 0
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = [
            executor.submit(
                correctness_check,
                solution,
                task_id.split("/")[0].lower(),
                ctask,
                expected_output,
            )
            for solution in samples
        ]
        for future in as_completed(futures):
            result, solution = future.result()
            ret_dict["results"].append(
                {
                    "solution": solution,
                    "pass": result[0] == PASS,
                    "matching_cluster_idx": None,
                }
            )
            n_passing += result[0] == PASS

    ret_dict["pass@1"] = n_passing / len(samples) * 100
    if n_passing < min_correct:
        print(f"{task_id}: {n_passing} < {min_correct} correct solutions, skipped")
        return ret_dict

    ######################### Profiling #########################
    pe_input = (
        mbpp_deserialize_inputs(task_id, ptask["pe_input"])[0]
        if task_id.startswith("Mbpp/")
        else ptask["pe_input"][0]
    )

    ####################################################################
    ############### Lazily profile reference solutions #################
    ####################################################################
    cache_ref_num_inst = [None] * n_reference

    def get_avg_ref_profile(index, check_order=True) -> Optional[Tuple]:
        nonlocal cache_ref_num_inst

        assert (
            index < n_reference - 1
            and cache_ref_num_inst[index + 1] is not None
            or index == n_reference - 1
        ), f"Calling get_avg_ref_profile({index}) before get_avg_ref_profile({index+1}) is called, is not allowed! {n_reference = }"

        if cache_ref_num_inst[index] is not None:
            return cache_ref_num_inst[index], ptask["scores"][index]

        evaluation_time = EVALUATION_TIMEOUT_SECOND_PER_TEST
        ref_solution = ptask["reference"][index]
        for _ in range(_REFERENCE_EXEC_TIMES):
            profiles = profile(
                ref_solution,
                entry_point,
                [pe_input],
                timeout_second_per_test=evaluation_time,
            )

            # Bad thing#1: timeout / failure happens
            if are_profiles_broken(profiles):
                print(f"{task_id}: [WARNING] Error in ref: {profiles}")
                rich.print(Syntax(ref_solution, "python"))
                print(f"{task_id}: Retrying w/ +5s timeout...")
                evaluation_time += 5
                continue

            avg_profile = mean(profiles)
            # Bad thing#2: if the current #instruction is faster than that of i+1
            if index < n_reference - 1 and avg_profile < cache_ref_num_inst[index + 1]:
                print(f"{task_id}: [WARNING] {index} ref faster than {index + 1}")
                rich.print(Syntax(ref_solution, "python"))
                print(
                    f"{task_id}: Ref {index+1} avg. #inst {cache_ref_num_inst[index+1]}"
                )
                print(f"{task_id}: Current solution mean runtime: {profiles}")
                if check_order:
                    return None

        cache_ref_num_inst[index] = avg_profile
        ret_dict["ref"][index]["_num_cpu_instructions"] = avg_profile
        return cache_ref_num_inst[index], ptask["scores"][index]

    ####################################################################
    ############################## END #################################
    ####################################################################

    if not lazy_evaluation:  # compute everything ahead of time
        for i in range(n_reference - 1, -1, -1):
            if get_avg_ref_profile(i) is None:
                break

        assert (
            None not in cache_ref_num_inst
        ), f"{task_id}: Failed to profile certain reference: {cache_ref_num_inst = }"

    for result in ret_dict["results"]:
        if not result["pass"]:
            continue

        sample_profiles = profile(
            solution,
            entry_point,
            [pe_input],
            timeout_second_per_test=EVALUATION_TIMEOUT_SECOND_PER_TEST,
        )

        score = 0
        norm_score = 0
        result["matching_cluster_idx"] = -1  # -1 means even slower than the slowest ref
        # if the solution results in a timeout, score is 0
        if are_profiles_broken(sample_profiles):
            print(
                f"{task_id}: Tested solution error'ed out: {sample_profiles} ... regarded as 0 score"
            )
            rich.print(Syntax(solution, "python"))
        else:
            avg_sample_profile = result["_num_cpu_instructions"] = mean(sample_profiles)

            # Get profiles from fast to slow:
            for j in range(n_reference - 1, -1, -1):
                avg_ref_profile, ref_score = get_avg_ref_profile(j, check_order=False)
                if avg_sample_profile <= avg_ref_profile:
                    result["matching_cluster_idx"] = j
                    score = ref_score
                    norm_score = 100 * (j + 1) / n_reference
                    break

        result["dps"] = score
        result["dps_norm"] = norm_score

    ret_dict["dps"] = mean(
        [r["dps"] for r in ret_dict["results"] if r["dps"] is not None]
    )
    ret_dict["dps_norm"] = mean(
        [r["dps_norm"] for r in ret_dict["results"] if r["dps_norm"] is not None]
    )

    print(
        f"\t{task_id}: {n_passing} / {len(samples)} correct solutions, "
        f"avg DPS: {ret_dict['dps'] :.1f}, avg DPS_norm: {ret_dict['dps_norm'] :.1f}"
    )

    return ret_dict


# TODO(@ganler): OPTIMIZATION: reuse the samples from the generations of other datasets
def script(
    samples: Optional[str] = None,
    min_correct: int = 10,
    n_samples: int = 100,
    temperature: float = 1.0,
    parallel: Optional[int] = None,
    lazy_evaluation: bool = True,
    i_just_wanna_run: bool = False,
    **model_kwargs,
):
    assert min_correct <= n_samples, "min_correct should be no more than max_n_samples"
    simple_test_profiler()  # test linux perf setup

    if model_kwargs:
        # overwrite parameters
        samples = run_codegen(
            dataset="evalperf",
            n_samples=n_samples,
            temperature=temperature,
            **model_kwargs,
        )

    assert samples is not None, "Please provide the path to the samples"

    if lazy_evaluation:
        rich.print(
            "[bold yellow]Lazy evaluation is enabled[/]: "
            "Fast evaluation without enumeratively checking reference order consistency."
        )

    # Data loading
    problems, expected_output = get_evalplus_data()
    ptasks = get_evalperf_data()

    # Parallelism
    max_workers = parallel or max(1, multiprocessing.cpu_count() // 4)
    assert 0 < max_workers < multiprocessing.cpu_count(), "Invalid max CPU workers"

    if os.path.isdir(samples):
        result_path = os.path.join(samples, "evalperf_results.json")
    else:
        assert samples.endswith(".jsonl")
        result_path = samples.replace(".jsonl", "_evalperf_results.json")

    # resume results
    eval_results = {}
    if not i_just_wanna_run and os.path.exists(result_path):
        eval_results = json.load(open(result_path, "r"))
        # pop tasks that have been evaluated
        for evaluated_task in eval_results:
            ptasks.pop(evaluated_task, None)

        rich.print(f"Resumed {len(eval_results)} results from {result_path}")

    # Load model's samples: task_id -> a list of samples
    temp_samples = defaultdict(list)
    for task in stream_jsonl(samples):
        task_id = task["task_id"].replace("_", "/")
        if len(temp_samples[task_id]) < n_samples:
            temp_samples[task_id].append(task["solution"])
    samples = temp_samples

    # assert each task has n_samples
    for task_id, task_samples in samples.items():
        assert (
            len(task_samples) == n_samples
        ), f"{task_id} has {len(task_samples)} samples != {n_samples}"

    # log all tasks
    rich.print(f"{len(ptasks)} tasks to evaluate :: result path: {result_path}")
    rich.print(f"Max CPU: {max_workers}")
    rich.print(f"{n_samples} samples per task")
    rich.print(f"Those with >= {min_correct} correct samples will be evalperf-ed")
    rich.print(f"Tasks: {list(ptasks.keys())}")

    TEST_MAX_WORKERS = min(max_workers, 4)
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                worker_on_one_task,
                task_id,
                ptask,
                samples[task_id],
                problems[task_id],
                expected_output[task_id],
                min_correct,
                TEST_MAX_WORKERS,
                lazy_evaluation,
            )
            for task_id, ptask in ptasks.items()
        ]

        with progress() as p:
            for future in p.track(as_completed(futures), total=len(futures)):
                result = future.result()
                eval_results[result["task_id"]] = result

    with open(result_path, "w") as f:  # final write
        f.write(json.dumps(eval_results))

    summarize_evalperf(eval_results)

    with open(result_path, "w") as f:
        f.write(
            json.dumps(
                {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "n_samples": n_samples,
                    "temperature": temperature,
                    "min_correct": min_correct,
                    "eval": eval_results,
                }
            )
        )


def main():
    from fire import Fire

    Fire(script)


if __name__ == "__main__":
    main()

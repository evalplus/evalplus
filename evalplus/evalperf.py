"""Compute the Differential Performance Scores (DPS) and DPS_{norm} of given samples from a model.
"""

import json
import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, List, Optional, Tuple

import numpy as np
from rich.console import Console
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.syntax import Syntax

from evalplus.data import (
    get_human_eval_plus,
    get_human_eval_plus_hash,
    get_mbpp_plus,
    get_mbpp_plus_hash,
)
from evalplus.data.mbpp import mbpp_deserialize_inputs
from evalplus.data.utils import stream_jsonl
from evalplus.eval import PASS, estimate_pass_at_k, untrusted_check
from evalplus.eval._special_oracle import MBPP_OUTPUT_NOT_NONE_TASKS
from evalplus.evaluate import get_groundtruth
from evalplus.perf.config import EVALUATION_TIMEOUT_SECOND_PER_TEST
from evalplus.perf.profile import are_profiles_broken, profile

_REFERENCE_EXEC_TIMES = 3


def check_solution(
    index: int, solution: str, dataset: str, task: Dict, expected_output: List
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
    return index, result, solution


def get_evalplus_data():
    problems_human = get_human_eval_plus(noextreme=True)
    dataset_hash = get_human_eval_plus_hash(noextreme=True)
    expected_output_human = get_groundtruth(problems_human, dataset_hash, [])
    problems_mbpp = get_mbpp_plus(noextreme=True)
    dataset_hash = get_mbpp_plus_hash(noextreme=True)
    expected_output_mbpp = get_groundtruth(
        problems_mbpp,
        dataset_hash,
        MBPP_OUTPUT_NOT_NONE_TASKS,
    )
    problems = {**problems_human, **problems_mbpp}
    expected_output = {**expected_output_human, **expected_output_mbpp}
    return problems, expected_output


def worker_on_one_task(
    task_id: str,
    task_ref: Dict,
    samples: list,
    task: Dict,
    expected_output: Dict,
    profile_n_correct: int,
    n_workers: int,
    lazy_evaluation: bool,
):
    console = Console()
    console.print(f"Processing task: {task_id}")
    # check correctness of the solutions
    correct_solutions = []
    correct_sample_ids = []
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = [
            executor.submit(
                check_solution,
                index,
                solution,
                task_id.split("/")[0].lower(),
                task,
                expected_output,
            )
            for index, solution in enumerate(samples)
        ]
        for future in as_completed(futures):
            index, result, solution = future.result()
            if result[0] == PASS:
                correct_solutions.append(solution)
            correct_sample_ids.append(index)

    if len(correct_solutions) == 0:
        console.print(f"{task_id}: 0 correct solutions")
        ret_dict = {
            "task_id": task_id,
            # basic
            "samples": samples,
            "correct_sample_ids": correct_sample_ids,
            # perf
            "dps": None,
            "dps_norm": None,
            "profiled_sample_ids": None,
            "profiled_num_instruction": None,
            "reference_num_instruction": None,
        }
        return ret_dict

    # make the order of the correct solutions consistent according to their original order
    correct_solutions = sorted(correct_solutions, key=lambda x: samples.index(x))

    # profile the model's solutions, and calculate the scores
    profiled_sample_ids = correct_sample_ids[:profile_n_correct]
    profiled_samples = correct_solutions[:profile_n_correct]

    # from slow to fast & from large to small
    n_reference = len(task_ref["reference"])
    pe_input = (
        mbpp_deserialize_inputs(task_id, task_ref["pe_input"])[0]
        if task_id.startswith("Mbpp/")
        else task_ref["pe_input"][0]
    )

    ####################################################################
    ############### Lazily profile reference solutions #################
    ####################################################################
    cache_ref_num_inst = [None] * n_reference

    def get_reference_profile(index, check_order=True) -> Optional[Tuple]:
        nonlocal cache_ref_num_inst

        assert (
            index < n_reference - 1
            and cache_ref_num_inst[index + 1] is not None
            or index == n_reference - 1
        ), f"Calling get_reference_profile({index}) before get_reference_profile({index+1}) is called, is not allowed! {n_reference = }"

        if cache_ref_num_inst[index] is not None:
            return cache_ref_num_inst[index], task_ref["scores"][index]

        evaluation_time = EVALUATION_TIMEOUT_SECOND_PER_TEST
        for _ in range(_REFERENCE_EXEC_TIMES):
            profiles = profile(
                task_ref["reference"][index],
                task["entry_point"],
                [pe_input],
                timeout_second_per_test=evaluation_time,
            )

            # Bad thing#1: timeout / failure happens
            if are_profiles_broken(profiles):
                console.print(f"{task_id}: [WARNING] Error in ref: {profiles}")
                console.print(Syntax(solution, "python"))
                console.print(f"{task_id}: Retrying w/ +5s timeout...")
                evaluation_time += 5
                continue

            # Bad thing#2: if the current #instruction is faster than that of i+1
            if index < n_reference - 1 and profiles < cache_ref_num_inst[index + 1]:
                console.print(
                    f"{task_id}: [WARNING] {index} ref faster than {index + 1}"
                )
                console.print(Syntax(solution, "python"))
                console.print(
                    f"{task_id}: Ref {index+1} avg. #inst {cache_ref_num_inst[index+1]}"
                )
                console.print(f"{task_id}: Current solution mean runtime: {profiles}")
                if check_order:
                    return None

        cache_ref_num_inst[index] = profiles
        return cache_ref_num_inst[index], task_ref["scores"][index]

    ####################################################################
    ############################## END #################################
    ####################################################################

    if not lazy_evaluation:  # compute everything ahead of time
        for i in range(n_reference - 1, -1, -1):
            if get_reference_profile(i) is None:
                break

        assert (
            None in cache_ref_num_inst
        ), f"{task_id}: Failed to profile reference: {cache_ref_num_inst = }"

    dps_scores = []
    dps_norm_scores = []
    profiled_num_inst = []
    for solution in profiled_samples:
        profiles = profile(
            solution,
            task["entry_point"],
            [pe_input],
            timeout_second_per_test=EVALUATION_TIMEOUT_SECOND_PER_TEST,
        )

        score = 0
        norm_score = 0

        # if the solution results in a timeout, score is 0
        if are_profiles_broken(profiles):
            console.print(f"{task_id}: Evaluated solution error'ed out: {profiles}")
            console.print(Syntax(solution, "python"))
        else:  # Get profiles from fast to slow:
            for j in range(n_reference - 1, -1, -1):
                ref_profile, ref_score = get_reference_profile(j, check_order=False)
                if profiles <= ref_profile:
                    score = ref_score
                    norm_score = 100 * (j + 1) / n_reference
                    break

        dps_scores.append(score)
        dps_norm_scores.append(norm_score)
        profiled_num_inst.append(profiles)

    console.print(
        f"{task_id}: {len(correct_solutions)} correct solutions, "
        f"average DPS: {float(np.mean(dps_scores)):.1f}, "
        f"average DPS_norm: {float(np.mean(dps_norm_scores)):.1f}"
    )

    return {
        "task_id": task_id,
        # basic
        "samples": samples,
        "correct_sample_ids": correct_sample_ids,
        # perf
        "dps": dps_scores,
        "dps_norm": dps_norm_scores,
        "profiled_sample_ids": profiled_sample_ids,
        "profiled_num_instruction": profiled_num_inst,
        "reference_num_instruction": cache_ref_num_inst,
    }


def script(
    samples: str,
    dataset: str,
    output_dir: str,
    profile_n_correct: int = 10,
    max_n_samples: int = 50,
    max_parallelism: int = None,
    lazy_evaluation: bool = False,
    i_just_wanna_run: bool = False,
):
    assert (
        profile_n_correct <= max_n_samples
    ), "profile_n_correct should be no more than max_n_samples"
    assert dataset.endswith(".jsonl") and os.path.isfile(dataset)
    assert samples.endswith(".jsonl") and os.path.isfile(samples)

    console = Console()  # printer

    if lazy_evaluation:
        console.print(
            "Lazy evaluation is enabled: "
            "It's faster but cannot address the order inconsistency on noisy testbed."
        )

    # load evalplus data
    problems, expected_output = get_evalplus_data()

    # load evalperf data
    with open(dataset, "r") as f:
        raw_data = [json.loads(l) for l in f]
        tasks = {task["task_id"]: task for task in raw_data}

    # setup max CPU threads
    max_workers = max(1, multiprocessing.cpu_count() // 4)
    if max_parallelism is not None:
        max_workers = min(max_workers, max_parallelism)

    model_name = os.path.basename(samples).replace(".jsonl", "")
    result_path = os.path.join(output_dir, f"{(model_name + '_results')}.json")

    # resume results
    eval_results = {}
    if not i_just_wanna_run and os.path.exists(result_path):
        eval_results = json.load(open(result_path, "r"))
        # pop tasks that have been evaluated
        for evaluated_task in eval_results:
            tasks.pop(evaluated_task, None)

        console.print(f"Resumed {len(eval_results)} results from {result_path}")

    # load model's solutions
    samples = {
        task["task_id"].replace("_", "/"): task["solution"][:max_n_samples]
        for task in stream_jsonl(samples)
    }

    # log all tasks
    console.print(f"{len(tasks)} tasks to evaluate :: result path: {result_path}")
    console.print(f"Model: {model_name}")
    console.print(f"Max CPU: {max_workers}")
    console.print(f"Max {max_n_samples} samples to check correctness per task")
    console.print(f"Of these, max {profile_n_correct} correct ones will be profiled")
    console.print(f"Tasks: {list(tasks.keys())}")

    progress_bar = Progress(
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
        TextColumn("•"),
        TimeRemainingColumn(),
    )

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                worker_on_one_task,
                task_id,
                task_ref,
                samples[task_id],
                problems[task_id],
                expected_output[task_id],
                profile_n_correct,
                max_workers,
                lazy_evaluation,
            )
            for task_id, task_ref in tasks.items()
        ]

        with progress_bar as p:
            for future in p.track(as_completed(futures), total=len(futures)):
                result = future.result()
                eval_results[result["task_id"]] = result

        with open(result_path, "w") as f:  # final write
            f.write(json.dumps(eval_results))

    # estimate pass@1
    total, correctness = zip(
        *[
            (len(task["samples"]), len(task["correct_sample_ids"]))
            for task in eval_results.values()
        ]
    )
    for task, pass_at_1 in zip(
        eval_results.keys(), estimate_pass_at_k(total, correctness, 1)
    ):
        eval_results[task]["pass@1"] = pass_at_1

    with open(result_path, "w") as f:
        f.write(json.dumps(eval_results))


def main():
    from fire import Fire

    Fire(script)


if __name__ == "__main__":
    main()

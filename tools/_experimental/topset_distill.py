import json
import os

import numpy as np

from evalplus.data import get_human_eval_plus, get_human_eval_plus_inputs

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=str, default="/JawTitan/EvalPlus/humaneval")
    args = parser.parse_args()

    plus_inputs = get_human_eval_plus_inputs()
    problems = get_human_eval_plus().values()

    base_bvs = {}
    plus_bvs = {}
    id2idx = {}

    for i, problem in enumerate(problems):
        task_id = problem["task_id"]
        id2idx[task_id] = i
        base_bvs[task_id] = np.zeros(len(problem["base_input"]), dtype=bool)
        plus_bvs[task_id] = np.zeros(len(plus_inputs[task_id]), dtype=bool)

    for path in os.listdir(args.root):
        eval_json_path = os.path.join(args.root, path, "eval_results.json")
        if not os.path.isfile(eval_json_path) or not path[-1].isdigit():
            print(f"skip {path}")
            continue
        res = json.load(open(eval_json_path, "r"))["eval"]

        for task_id, v in res.items():
            for status, details in v["base"]:
                if details is None:  # all fail => skip
                    continue
                fails = np.logical_not(details)
                base_bvs[task_id][: len(details)] = np.logical_xor(
                    base_bvs[task_id][: len(details)], fails
                )
            for status, details in v["plus"]:
                if details is None:
                    continue
                fails = np.logical_not(details)
                plus_bvs[task_id][: len(details)] = np.logical_xor(
                    plus_bvs[task_id][: len(details)], fails
                )

    testsuite = []

    new_sizes = []
    for task_id, bbv in base_bvs.items():
        new_inputs = []
        idx = id2idx[task_id]
        for i in np.nonzero(bbv)[0]:
            new_inputs.append(problems[idx]["base_input"][i])
        pbv = plus_bvs[task_id]
        for i in np.nonzero(pbv)[0]:
            new_inputs.append(plus_inputs[task_id][i])
        testsuite.append({"task_id": task_id, "inputs": new_inputs})
        print(
            task_id, f" org base {len(bbv)}; org plus {len(pbv)}; new {len(new_inputs)}"
        )
        new_sizes.append(len(new_inputs))

    new_sizes = np.array(new_sizes)
    print(f"{new_sizes.mean() = }, {new_sizes.min() = }, {new_sizes.max() = }")

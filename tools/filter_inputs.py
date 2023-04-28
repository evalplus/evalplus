import json
import os
from importlib import import_module

from eval_plus.utils import get_human_eval_plus, get_human_eval_plus_original_inputs

problems = get_human_eval_plus()
task_inputs = get_human_eval_plus_original_inputs()

new_input_path = "HumanEvalPlusInputsType_filtered.jsonl"


def execute(fn, input_list) -> bool:
    try:
        fn(*input_list)
    except Exception as e:
        assert str(e) == "invalid inputs"
        return False
    return True


def write(new_input_dict):
    with open(new_input_path, "a") as f:
        f.write(json.dumps(new_input_dict) + "\n")


assert not os.path.exists(new_input_path)
for i, p in enumerate(problems):
    entry_point = p["entry_point"]
    mod = import_module(f"groundtruth.{str(i).zfill(3)}_{entry_point}")
    fn = getattr(mod, entry_point)
    task_id = p["task_id"].replace("/", "_")
    new_inputs = task_inputs[task_id]
    count = 0
    new_input_dict = {"task_id": task_id, "inputs": []}
    for input_list in new_inputs:
        res = execute(fn, input_list)
        if res:
            new_input_dict["inputs"].append(input_list)
        else:
            count += 1
    write(new_input_dict)
    if count != 0:
        print(f"Task {task_id}: {count}/{len(new_inputs)} tests filtered")

# Convert a directory of solutions to a JSONL file

import json
import os

from tqdm import tqdm

from evalplus.data import get_human_eval_plus, get_mbpp_plus
from evalplus.sanitize import sanitize


def main(directory, sanitize_code: bool = True):
    basename = os.path.basename(directory)
    parent_dir = os.path.dirname(directory)
    target_jsonl_path = os.path.join(parent_dir, f"{basename}.jsonl")

    datasets = {**get_human_eval_plus(), **get_mbpp_plus()}

    with open(target_jsonl_path, "w") as f:
        # iterate directories
        for subdir_name in tqdm(os.listdir(directory)):
            subdir_path = os.path.join(directory, subdir_name)
            if not os.path.isdir(subdir_path):
                continue

            assert "_" in subdir_name
            dataset_name, task_num = subdir_name.split("_")
            task_id = f"{dataset_name}/{task_num}"
            entrypoint = datasets[task_id]["entry_point"]
            for sample_name in os.listdir(subdir_path):
                if not sample_name.endswith(".py"):
                    continue
                code = open(os.path.join(subdir_path, sample_name)).read()
                if sanitize_code:
                    try:
                        code = sanitize(code, entrypoint=entrypoint)
                    except ValueError as e:
                        print(f"Failed to sanitize {task_id}/{sample_name}: {e}")
                        print(code)
                        continue

                f.write(json.dumps({"task_id": task_id, "solution": code}) + "\n")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)

import json
import os

from datasets import Dataset, DatasetDict
from fire import Fire
from huggingface_hub import create_tag, delete_tag, list_repo_refs

from evalplus.data import get_human_eval_plus, get_mbpp_plus

REPO_ID = "evalplus/evalperf"


def main(path, overwrite=False):
    assert path.endswith(".jsonl"), f"{path} is not a jsonl file"
    name = os.path.basename(path).split(".")[0]
    first, version = name.split("-")
    assert first == "evalperf", f"Expected fmt evalperf-[date].jsonl; but got {path}"

    evalplus_datasets = {**get_human_eval_plus(), **get_mbpp_plus()}

    with open(path, "r") as f:
        data = [json.loads(line) for line in f]

    # drop task ids that are removed in latest EvalPlus dataset
    to_drop = [
        task["task_id"] for task in data if task["task_id"] not in evalplus_datasets
    ]
    print(f"Removing {len(to_drop)} tasks that are not in the latest EvalPlus dataset")
    print(to_drop)
    data = [d for d in data if d["task_id"] not in to_drop]

    # convert pe_input into string
    for d in data:
        d["pe_input"] = json.dumps(d["pe_input"])
        d["entry_point"] = evalplus_datasets[d["task_id"]]["entry_point"]
        d["prompt"] = evalplus_datasets[d["task_id"]]["prompt"]

    # combine
    dataset = DatasetDict(
        {
            "test": Dataset.from_list(data, split="test"),
            "demo": Dataset.from_list(data[:2], split="demo"),
        }
    )
    print(dataset)

    repo = list_repo_refs(REPO_ID, repo_type="dataset")
    tags = [tag.name for tag in repo.tags]
    print(REPO_ID, "has tags:", tags)

    print(f"Uploading dataset with tag {version} to Hub... Please enter to confirm:")
    input()

    if version in tags and overwrite:
        print(f"Tag {version} already exists, overwriting...")
        delete_tag(REPO_ID, repo_type="dataset", tag=version)

    dataset.push_to_hub(REPO_ID, branch="main")
    create_tag(REPO_ID, repo_type="dataset", tag=version)


if __name__ == "__main__":
    Fire(main)

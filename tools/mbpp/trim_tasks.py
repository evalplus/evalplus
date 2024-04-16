import json
import re

from rich.console import Console

from evalplus.data.mbpp import get_mbpp_plus, mbpp_serialize_inputs
from evalplus.data.utils import write_jsonl


def find_links(task_id: str, text: str) -> list:
    url_pattern = re.compile(r"https?://\S+[.\S]+")
    matches = url_pattern.findall(text)
    return matches


def main(args):
    console = Console()
    plus_problems = get_mbpp_plus(mini=False)

    removed = []

    for task_id, task in plus_problems.items():
        # trim tasks with links in prompt
        prompt = task["prompt"]
        matches = find_links(task_id, prompt)
        if matches:
            console.print(f"Removed {task_id} for having links in prompt.")
            removed.append(task_id)

    console.print(f"Totally removed {len(removed)} tasks with links in prompt.")

    with open(args.output_path, "w") as f:
        for task_id, task in plus_problems.items():
            if task_id not in removed:
                task["base_input"] = mbpp_serialize_inputs(task_id, task["base_input"])
                task["plus_input"] = mbpp_serialize_inputs(task_id, task["plus_input"])
                f.write(json.dumps(task) + "\n")


if __name__ == "__main__":
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--output-path", type=str, default="mbpp_plus_links_removed.jsonl"
    )
    args = argparser.parse_args()
    main(args)

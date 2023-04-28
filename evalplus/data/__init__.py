import gzip
import json
import os
from typing import Dict, List

import tempdir
import wget
from appdirs import user_cache_dir

CACHE_DIR = user_cache_dir("evalplus")


HUMANEVAL_URL = (
    "https://github.com/openai/human-eval/raw/master/data/HumanEval.jsonl.gz"
)
HUMANEVAL_PLUS_URL = "https://raw.githubusercontent.com/ganler/release/main/dataset/HumanEvalPlus/HumanEvalPlus-v0.1.0.jsonl.gz"


# hacky way to handle \n\r, etc in strings
def to_raw(string):
    return string.encode("unicode-escape").decode().replace("\\\\", "\\")


def get_human_eval_plus(err_incomplete=True) -> List[Dict[str, str]]:
    """Get HumanEvalPlus locally.
    Args:
        err_incomplete (bool, optional): Whether to raise error if HumanEvalPlus is not complete. Defaults to True.
    Returns:
        List[Dict[str, str]]: List of dicts with keys "task_id", "prompt", "contract", "canonical_solution", "base_input"
    Notes:
        "task_id" is the identifier string for the task
        "prompt" is the function signature with docstring
        "contract" is the assertions for the function's input (validity)
        "canonical_solution" is the ground-truth implementation for diff-testing
        "base_input" is the test inputs from original HumanEval
        "plus_input" is the test inputs brought by EvalPlus
        "atol" is the absolute tolerance for diff-testing
    """
    # Check if human eval file exists in CACHE_DIR
    plus_path = os.path.join(CACHE_DIR, "HumanEval.jsonl")

    plus = None
    if not os.path.exists(plus_path):
        # Install HumanEval dataset and parse as jsonl
        # https://github.com/openai/human-eval/blob/master/data/HumanEval.jsonl.gz
        print("Downloading HumanEvalPlus dataset...")
        with tempdir.TempDir() as tmpdir:
            plus_gz_path = os.path.join(tmpdir, "HumanEvalPlus.jsonl.gz")
            wget.download(HUMANEVAL_PLUS_URL, plus_gz_path)

            with gzip.open(plus_gz_path, "rb") as f:
                plus = f.read().decode("utf-8")

        # create CACHE_DIR if not exists
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)

        # Write the original human eval file to CACHE_DIR
        with open(plus_path, "w") as f:
            f.write(plus)

    plus = open(plus_path, "r").read() if not plus else plus
    plus = plus.split("\n")
    plus = [json.loads(line) for line in plus if line]
    if err_incomplete:
        for task in plus:
            task_id = task["task_id"]
            for key in [
                "prompt",
                "contract",
                "canonical_solution",
                "base_input",
                "plus_input",
                "atol",
            ]:
                assert key in task, f"{key} not found in HumanEvalPlus #{task_id}!"
    return plus


def get_human_eval() -> List[Dict[str, str]]:
    """Get HumanEval from OpenAI's github repo and return as a list of parsed dicts.

    Returns:
        List[Dict[str, str]]: List of dicts with keys "prompt", "test", "entry_point"

    Notes:
        "task_id" is the identifier string for the task.
        "prompt" is the prompt to be used for the task (function signature with docstrings).
        "test" is test-cases wrapped in a `check` function.
        "entry_point" is the name of the function.
    """
    # Check if human eval file exists in CACHE_DIR
    human_eval_path = os.path.join(CACHE_DIR, "HumanEval.jsonl")

    human_eval = None
    if not os.path.exists(human_eval_path):
        # Install HumanEval dataset and parse as jsonl
        # https://github.com/openai/human-eval/blob/master/data/HumanEval.jsonl.gz
        print("Downloading HumanEval dataset...")
        with tempdir.TempDir() as tmpdir:
            human_eval_gz_path = os.path.join(tmpdir, "HumanEval.jsonl.gz")
            wget.download(HUMANEVAL_URL, human_eval_gz_path)

            with gzip.open(human_eval_gz_path, "rb") as f:
                human_eval = f.read().decode("utf-8")

        # create CACHE_DIR if not exists
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)

        # Write the original human eval file to CACHE_DIR
        with open(human_eval_path, "w") as f:
            f.write(human_eval)

    human_eval = open(human_eval_path, "r").read() if not human_eval else human_eval
    human_eval = human_eval.split("\n")
    human_eval = [json.loads(line) for line in human_eval if line]

    # Handle 115_max_fill.py to make its docstring well-formed
    human_eval[114]["prompt"] = "import math\n" + human_eval[114]["prompt"].replace(
        "import math\n", ""
    )

    return human_eval

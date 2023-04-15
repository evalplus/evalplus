import os
import tempdir
import gzip
import json
from typing import List, Dict

import wget
from appdirs import user_cache_dir

CACHE_DIR = user_cache_dir("fuzz-eval")


def get_human_eval() -> List[Dict[str, str]]:
    """Get human eval dataset from OpenAI's github repo and return as a list of parsed dicts.

    Returns:
        List[Dict[str, str]]: List of dicts with keys "prompt", "test", "entry_point"

    Notes:
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
        human_eval_gz_path = os.path.join(tmpdir, "HumanEval.jsonl.gz")
        with tempdir.TempDir() as tmpdir:
            wget.download(
                "https://github.com/openai/human-eval/raw/master/data/HumanEval.jsonl.gz",
                human_eval_gz_path,
            )

        with gzip.open(human_eval_gz_path, "rb") as f:
            human_eval = f.read().decode("utf-8")

        # Write the original human eval file to CACHE_DIR
        with open(human_eval_path, "w") as f:
            f.write(human_eval)

    human_eval = open(human_eval_path, "r").read() if not human_eval else human_eval
    human_eval = human_eval.split("\n")
    human_eval = [json.loads(line) for line in human_eval if line]
    return human_eval

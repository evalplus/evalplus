import hashlib
import json
import os
from typing import Dict

from evalplus.data.utils import (
    CACHE_DIR,
    completeness_check,
    get_dataset_metadata,
    make_cache,
    stream_jsonl,
)

HUMANEVAL_PLUS_VERSION = "v0.1.10"
HUMANEVAL_OVERRIDE_PATH = os.environ.get("HUMANEVAL_OVERRIDE_PATH", None)


def _ready_human_eval_plus_path(mini=False, noextreme=False, version="default") -> str:
    if HUMANEVAL_OVERRIDE_PATH:
        return HUMANEVAL_OVERRIDE_PATH

    version = HUMANEVAL_PLUS_VERSION if version == "default" else version
    url, plus_path = get_dataset_metadata(
        "HumanEvalPlus", HUMANEVAL_PLUS_VERSION, mini, noextreme
    )
    make_cache(url, plus_path)

    return plus_path


def get_human_eval_plus_hash(mini=False, noextreme=False, version="default") -> str:
    """Get the hash of HumanEvalPlus.
    Returns:
        str: The hash of HumanEvalPlus
    """
    plus_path = _ready_human_eval_plus_path(mini, noextreme, version="default")
    with open(plus_path, "rb") as f:
        plus = f.read()
    return hashlib.md5(plus).hexdigest()


def get_human_eval_plus(
    err_incomplete=True, mini=False, noextreme=False, version="default"
) -> Dict[str, Dict]:
    """Get HumanEvalPlus locally.
    Args:
        err_incomplete (bool, optional): Whether to raise error if HumanEvalPlus is not complete. Defaults to True.
        mini (bool, optional): Whether to use the mini version of HumanEvalPlus. Defaults to False.
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
    plus_path = _ready_human_eval_plus_path(
        mini=mini, noextreme=noextreme, version=version
    )
    plus = {task["task_id"]: task for task in stream_jsonl(plus_path)}
    if err_incomplete:
        completeness_check("HumanEval+", plus)
    return plus


def get_human_eval() -> Dict[str, Dict]:
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
    make_cache(
        "https://github.com/openai/human-eval/raw/master/data/HumanEval.jsonl.gz",
        human_eval_path,
    )

    human_eval = open(human_eval_path, "r").read().split("\n")
    human_eval = [json.loads(line) for line in human_eval if line]

    # Handle 115_max_fill.py to make its docstring well-formed
    human_eval[115]["prompt"] = "import math\n" + human_eval[115]["prompt"].replace(
        "import math\n", ""
    )

    return {task["task_id"]: task for task in human_eval}

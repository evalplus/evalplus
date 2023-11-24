"""
This script aims at quickly initialize a sketch for HumanEvalPlus. It's not going to be
perfect, but we will either manually or automatically fix/complete it later.
+ CHANGE 1: Adds "contract", "base_input", "atol" in addition to HumanEval.
"""

import json
import os
import pathlib
from importlib import import_module
from inspect import getsource
from typing import Tuple

from tempdir import TempDir

from evalplus.data.humaneval import get_human_eval

HUMANEVAL_PLUS_PATH = (
    pathlib.Path(__file__).parent.parent.parent / "HumanEvalPlus.jsonl"
)


def _ret(entry_point) -> str:
    """This is a hacky function to return some garbages so that we can
    successfully run the function .
    """
    if entry_point == "sort_third" or entry_point == "sort_even":
        return [1, 2, 3]
    elif entry_point == "bf":
        return ()
    return "1"


def instrument_inputs(entry_point, prompt, test) -> str:
    globals()["_inputs"] = []
    fn_text = f"""{prompt.split(f"def {entry_point}")[0]}

def {entry_point}(*args):
    _inputs.append(args)
    return {_ret(entry_point)}
"""
    exec(fn_text, globals())
    exec(test.replace("assert ", ""), globals())
    exec(f"check({entry_point})", globals())
    exec(fn_text, globals())
    return globals()["_inputs"]


def get_contract_and_ref(task_id: int, entry_point) -> Tuple[str, str]:
    mod = import_module(f"groundtruth.humaneval.{str(task_id).zfill(3)}_{entry_point}")
    fn = getattr(mod, entry_point)

    doc = fn.__doc__
    if task_id == 51:
        doc = doc.replace("bcdf\nghjklm", r"bcdf\nghjklm").replace(
            "abcdef\nghijklm", r"abcdef\nghijklm"
        )

    code = (
        getsource(fn).replace(doc, "").replace("''''''", '""""""').split('""""""\n')[-1]
    )

    assert code, f"Something wrong with {task_id}!"
    assert code[:3] != "def", f"Something wrong with the {task_id}!"

    # split code to contract and impl
    contract = ""
    impl = ""

    reading_contract = True
    for line in code.strip("\n").split("\n"):
        if reading_contract and "$_CONTRACT_$" in line:
            contract += line + "\n"
        else:
            reading_contract = False
            impl += line + "\n"

    if contract:
        contract = "\n" + contract

    return contract, "\n" + impl + "\n"


def get_atol(task_id: int) -> float:
    if task_id == 2 or task_id == 4:
        return 1e-6
    elif task_id == 32:
        return 1e-4
    return 0


if __name__ == "__main__":
    assert not HUMANEVAL_PLUS_PATH.exists(), f"{HUMANEVAL_PLUS_PATH} already exists!"

    human_eval = get_human_eval()
    with TempDir() as temp_dir:
        tmp_file = os.path.join(temp_dir, HUMANEVAL_PLUS_PATH)
        with open(tmp_file, "w") as writer:
            for task in human_eval:
                task_id = int(task["task_id"].split("/")[-1])
                task["contract"], task["canonical_solution"] = get_contract_and_ref(
                    task_id, task["entry_point"]
                )
                task["base_input"] = instrument_inputs(
                    task["entry_point"], task["prompt"], task["test"]
                )
                task["atol"] = get_atol(task_id)
                task["task_id"] = task["task_id"]

                writer.write(json.dumps(task) + "\n")
        # move tmp_file to HUMANEVAL_PLUS_PATH
        os.rename(tmp_file, HUMANEVAL_PLUS_PATH)

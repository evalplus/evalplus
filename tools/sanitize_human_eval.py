"""
---------------------------------------------------------------------------------
HumanEval's format is basically:
- "task_id": identifier string for the task
- "prompt": function signature with docstring
- "test": a function called `def check(candidate):` with assertions as test-cases
- "entry_point": name of the function
---------------------------------------------------------------------------------
We want to have a better structure for HumanEvalPlus:
- "task_id", "prompt", "canonical_solution" and "entry_point" are the same
+ "base_input": test inputs for diff-testing
+ "atol": absolute tolerance for diff-testing
[NOTE] Above is something stable. For unstable part, i.e., fuzzer-generated inputs,
we will use another separate file to store them.
---------------------------------------------------------------------------------
This script aims at quickly set-up a sketch for HumanEvalPlus. It's not going to be
perfect, but we will either manually or automatically fix/complete it later.
"""

import json
from importlib import import_module
from inspect import getsource
from typing import Tuple

from eval_plus.utils import HUMANEVAL_PLUS_PATH, get_human_eval


def _ret(entry_point) -> str:
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


def get_contract_and_ref(task_id: str, entry_point) -> Tuple[str, str]:
    # FIXME: may just use `canonical_solution`
    mod = import_module(f"groundtruth_bk.{task_id.zfill(3)}_{entry_point}")
    fn = getattr(mod, entry_point)

    doc = fn.__doc__
    if task_id == "51":
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


def get_atol(task_id: str) -> float:
    if task_id == "002" or task_id == "004":
        return 1e-6
    elif task_id == "032":
        return 1e-4  # FIXME: actually wrapped by poly.
    return 0


if __name__ == "__main__":
    assert not HUMANEVAL_PLUS_PATH.exists(), f"{HUMANEVAL_PLUS_PATH} already exists!"

    human_eval = get_human_eval()
    with open(HUMANEVAL_PLUS_PATH, "w") as file:
        new = {}
        for old in human_eval:
            task_id = old["task_id"].split("/")[-1]
            new["contract"], new["reference"] = get_contract_and_ref(
                task_id, old["entry_point"]
            )
            new["base_input"] = instrument_inputs(
                old["entry_point"], old["prompt"], old["test"]
            )
            new["atol"] = get_atol(task_id)

            file.write(json.dumps(new) + "\n")

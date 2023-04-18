"""
---------------------------------------------------------------------------------
HumanEval's format is basically:
- "task_id": identifier string for the task
- "prompt": function signature with docstring
- "test": a function called `def check(candidate):` with assertions as test-cases
- "entry_point": name of the function
---------------------------------------------------------------------------------
We want to have a better structure for HumanEvalPlus:
- "task_id", "prompt" and "entry_point" are the same
+ "isignature": function's input signature in Dict[var_str, type_str].
+ "docstring": docstring
+ "canonical_solution": the ground-truth implementation for diff-testing
+ "base_input": test inputs
[NOTE] Above is something stable. For unstable part, i.e., fuzzer-generated inputs,
we will use another separate file to store them.
---------------------------------------------------------------------------------
This script aims at quickly set-up a sketch for HumanEvalPlus. It's not going to be
perfect, but we will either manually or automatically fix/complete it later.
"""

import json
from inspect import signature, getsource
from typing import Tuple
from importlib import import_module

from eval_plus.utils import HUMANEVAL_PLUS_PATH, get_human_eval


def extract_sig_and_docstr(entry_point, prompt) -> Tuple[str, str]:
    ldict = {}
    fn_text = prompt + "    pass"
    exec(fn_text, globals(), ldict)
    fn = ldict[entry_point]
    sig_dict = {}
    for var, param in signature(fn).parameters.items():
        ann = param.annotation
        if ann is param.empty:
            ann = "Any"
        elif ann in {int, str, float, bool, list, tuple, set, dict}:
            ann = ann.__name__

        ann = (
            f"{ann}".replace("typing.", "")
            .replace("dict", "Dict")
            .replace("list", "List")
            .replace("tuple", "Tuple")
            .replace("set", "Set")
        )
        sig_dict[var] = ann
    return sig_dict, fn.__doc__


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


if __name__ == "__main__":
    assert not HUMANEVAL_PLUS_PATH.exists(), f"{HUMANEVAL_PLUS_PATH} already exists!"

    human_eval = get_human_eval()
    with open(HUMANEVAL_PLUS_PATH, "w") as file:
        new = {}
        for old in human_eval:
            new["task_id"] = old["task_id"]
            new["prompt"] = old["prompt"]
            new["entry_point"] = old["entry_point"]

            new["isignature"], new["docstring"] = extract_sig_and_docstr(
                old["entry_point"], old["prompt"]
            )
            new["contract"], new["reference"] = get_contract_and_ref(
                old["task_id"].split("/")[-1], old["entry_point"]
            )
            new["canonical_solution"] = old["canonical_solution"]
            new["base_input"] = instrument_inputs(
                old["entry_point"], old["prompt"], old["test"]
            )

            file.write(json.dumps(new) + "\n")

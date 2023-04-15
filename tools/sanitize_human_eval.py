"""
---------------------------------------------------------------------------------
HumanEval's format is basically:
- "task_id": identifier string for the task
- "prompt": function signature with docstring
- "test": a function called `def check(candidate):` with assertions as test-cases
- "entry_point": name of the function
---------------------------------------------------------------------------------
We want to have a better structure for FuzzEval:
- "task_id", "prompt" and "entry_point" are the same
+ "isignature": function's input signature in Dict[var_str, type_str].
+ "docstring": docstring
+ "reference": the ground-truth implementation for diff-testing
+ "base_input": test inputs
[NOTE] Above is something stable. For unstable part, i.e., fuzzer-generated inputs,
we will use another separate file to store them.
---------------------------------------------------------------------------------
This script aims at quickly set-up a sketch for FuzzEval. It's not going to be
perfect, but we will either manually or automatically fix/complete it later.
"""

import json
import pathlib

from inspect import signature
from fuzz_eval.utils import get_human_eval, FUZZEVAL_PATH


def extract_sig_and_docstr(entry_point, prompt) -> str:
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


def get_reference(task_id, entry_point, promt) -> str:
    fname = (
        pathlib.Path(__file__).parent.parent
        / "groundtruth"
        / f"{task_id.zfill(3)}_{entry_point}.py"
    )
    code = None
    for p in open(fname, "r").read().split("\n\n\n"):
        p = p.strip()
        prefix = promt.split("\n\n\n")[-1].strip()
        if p.startswith(prefix):
            code = p.split(prefix)[-1]
            break

    assert code
    return code


if __name__ == "__main__":
    assert not FUZZEVAL_PATH.exists(), "FuzzEval.jsonl already exists!"

    human_eval = get_human_eval()
    with open(FUZZEVAL_PATH, "w") as file:
        new = {}
        for old in human_eval:
            new["task_id"] = old["task_id"]
            new["promt"] = old["prompt"]
            new["entry_point"] = old["entry_point"]

            new["isignature"], new["docstring"] = extract_sig_and_docstr(
                old["entry_point"], old["prompt"]
            )
            new["reference"] = get_reference(
                old["task_id"].split("/")[-1], old["entry_point"], old["prompt"]
            )
            new["base_input"] = instrument_inputs(
                old["entry_point"], old["prompt"], old["test"]
            )

            file.write(json.dumps(new) + "\n")

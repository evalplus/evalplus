import json
import sys
from argparse import ArgumentParser
from copy import deepcopy
from typing import Dict

import numpy as np
from rich.progress import track

from evalplus.data.humaneval import get_human_eval_plus, get_human_eval_plus_hash
from evalplus.eval._special_oracle import _poly
from evalplus.evaluate import get_groundtruth

HUMANEVAL_CHECK = """\
{imports}

{aux_fn}

def check(candidate):
    inputs = {inputs}
    exp_out = {expected_outputs}
    for inp, exp in zip(inputs, exp_out):
        {assertion}
"""

ASSERTION_FN = f"""\
import numpy as np

def is_floats(x) -> bool:
    # check if it is float; List[float]; Tuple[float]
    if isinstance(x, float):
        return True
    if isinstance(x, (list, tuple)):
        return all(isinstance(i, float) for i in x)
    if isinstance(x, np.ndarray):
        return x.dtype == np.float64 or x.dtype == np.float32
    return False

def assertion(out, exp, atol):
    exact_match = out == exp

    if atol == 0 and is_floats(exp):
        atol = 1e-6
    if not exact_match and atol != 0:
        np.testing.assert_allclose(out, exp, atol=atol)
    else:
        assert exact_match
"""


def is_floats(x) -> bool:
    # check if it is float | List[float] | Tuple[float] and not empty for sequence
    if isinstance(x, float):
        return True
    if isinstance(x, (list, tuple)) and len(x) > 0:
        return all(isinstance(i, float) for i in x)
    if isinstance(x, np.ndarray):
        return x.dtype == np.float64 or x.dtype == np.float32
    return False


def humaneval_checker(problem: Dict) -> str:
    assert len(problem["base_input"]) == len(problem["expected_output"]["base"])
    assert len(problem["plus_input"]) == len(problem["expected_output"]["plus"])
    inputs = problem["base_input"] + problem["plus_input"]
    expected_outputs = (
        problem["expected_output"]["base"] + problem["expected_output"]["plus"]
    )
    assert len(inputs) == len(expected_outputs)
    atol = problem["atol"]
    imports = set()
    aux_fn = ""
    if "find_zero" == problem["entry_point"]:
        import inspect

        imports.add("import math")
        aux_fn = inspect.getsource(_poly) + "\n"
        assertion = f"assert _poly(*candidate(*inp), inp) <= {atol}"
        return HUMANEVAL_CHECK.format(
            imports="\n".join(imports),
            aux_fn=aux_fn,
            inputs=inputs,
            expected_outputs=expected_outputs,
            assertion=assertion,
        )
    aux_fn = ASSERTION_FN
    assertion = f"assertion(candidate(*inp), exp, {atol})"
    return HUMANEVAL_CHECK.format(
        imports="\n".join(imports),
        aux_fn=aux_fn,
        inputs=inputs,
        expected_outputs=expected_outputs,
        assertion=assertion,
    )


def main():
    sys.set_int_max_str_digits(int(10e8))
    argparser = ArgumentParser()
    argparser.add_argument("--mini", action="store_true", default=False)
    args = argparser.parse_args()

    problems = get_human_eval_plus(mini=args.mini)
    compatible_problems = deepcopy(problems)
    dataset_hash = get_human_eval_plus_hash()
    expected_outputs = get_groundtruth(problems, dataset_hash, [])
    for task_id, problem in track(problems.items()):
        print(task_id)
        problem["expected_output"] = expected_outputs[task_id]
        compatible_problems[task_id]["test"] = humaneval_checker(problem)
    with open("compatible_humaneval_plus.jsonl", "w") as f:
        for problem in compatible_problems.values():
            problem.pop("contract")
            problem.pop("base_input")
            problem.pop("plus_input")
            f.write(json.dumps(problem) + "\n")


if __name__ == "__main__":
    main()

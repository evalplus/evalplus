import ast
import inspect
import json
import multiprocessing
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed

from tqdm import tqdm

from evalplus.data.humaneval import (
    HUMANEVAL_PLUS_VERSION,
    get_human_eval_plus,
    get_human_eval_plus_hash,
)
from evalplus.eval import is_floats
from evalplus.eval._special_oracle import _poly
from evalplus.evaluate import get_groundtruth

HUMANEVAL_TEST_TEMPLATE = """\
{imports}

{aux_fn}

def check(candidate):
    inputs = {inputs}
    results = {results}
    for i, (inp, exp) in enumerate(zip(inputs, results)):
        {assertion}
"""

HUMANEVAL_CROSSCHECK_TEMPLATE = """\
{aux_fn}

{ref_func}

def check(candidate):
    inputs = {inputs}
    for i, inp in enumerate(inputs):
        assertion(candidate(*inp), ref_func(*inp), {atol})
"""

ASSERTION_FN = f"""\
import numpy as np

{inspect.getsource(is_floats)}

def assertion(out, exp, atol):
    exact_match = out == exp

    if atol == 0 and is_floats(exp):
        atol = 1e-6
    if not exact_match and atol != 0:
        assert np.allclose(out, exp, rtol=1e-07, atol=atol)
    else:
        assert exact_match
"""


def synthesize_test_code(task_id, entry_point, inputs, results, ref_func, atol):
    # dataset size optimization for large outputs
    if entry_point in (
        "tri",
        "string_sequence",
        "starts_one_ends",
        "make_a_pile",
        "special_factorial",
        "all_prefixes",
    ):
        return task_id, HUMANEVAL_CROSSCHECK_TEMPLATE.format(
            aux_fn=ASSERTION_FN,
            inputs=inputs,
            ref_func=ref_func.replace(f" {entry_point}(", " ref_func("),
            atol=atol,
        )

    # default settings
    imports = set()
    aux_fn = ASSERTION_FN
    assertion = f"assertion(candidate(*inp), exp, {atol})"

    # special case: poly
    if entry_point == "find_zero":
        imports.add("import math")
        aux_fn = inspect.getsource(_poly) + "\n"
        assertion = f"assert _poly(*candidate(*inp), inp) <= {atol}"

    return task_id, HUMANEVAL_TEST_TEMPLATE.format(
        imports="\n".join(imports),
        aux_fn=aux_fn,
        inputs=inputs,
        results=results,
        assertion=assertion,
    )


def deduplicate(inputs, results):
    assert len(inputs) == len(results)
    unique_input_strs = set([f"{x}" for x in inputs])

    new_inputs, new_results = [], []
    for inp, res in zip(inputs, results):
        inp_str = f"{inp}"
        if inp_str in unique_input_strs:
            new_inputs.append(inp)
            new_results.append(res)
            unique_input_strs.remove(inp_str)

    return new_inputs, new_results


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug-tasks", nargs="+", default=[], type=int)

    args = parser.parse_args()

    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(int(10e8))

    plus_problems = get_human_eval_plus(mini=False)
    dataset_hash = get_human_eval_plus_hash()

    compatible_problems = {}
    expected_outputs = get_groundtruth(plus_problems, dataset_hash, [])

    # debugging: monitoring test code size
    id2bytes = {}

    n_workers = max(1, multiprocessing.cpu_count() // 4)
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = []
        for task_id, plus_form in tqdm(plus_problems.items()):
            if args.debug_tasks and int(task_id.split("/")[-1]) not in args.debug_tasks:
                continue

            compatible_form = {}
            compatible_form["task_id"] = task_id
            compatible_form["prompt"] = plus_form["prompt"]
            compatible_form["canonical_solution"] = plus_form["canonical_solution"]
            compatible_form["entry_point"] = plus_form["entry_point"]
            compatible_problems[task_id] = compatible_form

            inputs = plus_form["base_input"] + plus_form["plus_input"]
            results = (
                expected_outputs[task_id]["base"] + expected_outputs[task_id]["plus"]
            )

            inputs, results = deduplicate(inputs, results)

            assert len(inputs) == len(results)
            atol = plus_form["atol"]

            simplified_prompt = ""
            for line in compatible_form["prompt"].split("\n"):
                if not line:
                    continue
                if '"""' in line or "'''" in line:
                    break
                simplified_prompt += line + "\n"

            futures.append(
                executor.submit(
                    synthesize_test_code,
                    task_id,
                    compatible_form["entry_point"],
                    inputs,
                    results,
                    simplified_prompt + compatible_form["canonical_solution"],
                    atol,
                )
            )

        for future in tqdm(as_completed(futures), total=len(plus_problems)):
            task_id, test_code = future.result()
            # syntax check of test_code
            ast.parse(test_code)
            id2bytes[task_id] = len(test_code.encode("utf-8"))
            compatible_problems[task_id]["test"] = test_code

    # print the top-10 largest test code
    print("Top-10 largest test code comes from problems (in megabytes):")
    for task_id, size in sorted(id2bytes.items(), key=lambda x: x[1], reverse=True)[
        :10
    ]:
        print(f"{task_id}:\t{size / 1024 / 1024:.2f}mb")

    if args.debug_tasks:
        for problem in compatible_problems.values():
            print("--- debugging:", problem["task_id"])
            print(problem["prompt"] + problem["canonical_solution"])
            test_code = problem["test"]
            if len(test_code) <= 2048 + 512:
                print(test_code)
            else:
                print(problem["test"][:1024], "...")
                print("...", problem["test"][-1024:])
    else:
        with open(f"HumanEvalPlus-OriginFmt-{HUMANEVAL_PLUS_VERSION}.jsonl", "w") as f:
            for problem in compatible_problems.values():
                f.write(json.dumps(problem) + "\n")


if __name__ == "__main__":
    main()

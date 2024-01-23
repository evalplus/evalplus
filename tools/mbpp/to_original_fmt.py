import ast
import inspect
import json
import multiprocessing
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed

from tqdm import tqdm

from evalplus.data.mbpp import (
    MBPP_PLUS_VERSION,
    get_mbpp,
    get_mbpp_plus,
    get_mbpp_plus_hash,
)
from evalplus.eval import is_floats
from evalplus.eval._special_oracle import MBPP_OUTPUT_NOT_NONE_TASKS
from evalplus.evaluate import get_groundtruth

MBPP_TEST_TEMPLATE = """\
{imports}

{aux_fn}

inputs = {inputs}
results = {results}
for i, (inp, exp) in enumerate(zip(inputs, results)):
    assertion({entry_point}(*inp), exp, {atol})
"""

MBPP_CROSSCHECK_TEMPLATE = """\
{aux_fn}

{ref_func}

inputs = {inputs}
for i, inp in enumerate(inputs):
    assertion({entry_point}(*inp), ref_func(*inp), {atol})
"""

ASSERTION_FN = f"""\
import numpy as np

{inspect.getsource(is_floats)}

def assertion(out, exp, atol):
    exact_match = out == exp

    if atol == 0 and is_floats(exp):
        atol = 1e-6
    if not exact_match and atol != 0:
        np.testing.assert_allclose(out, exp, atol=atol)
    else:
        assert exact_match
"""


def synthesize_test_code(task_id, entry_point, inputs, results, ref_func, atol):
    # dataset size optimization for large outputs
    if entry_point in ("combinations_colors", "freq_count", "get_coordinates"):
        return task_id, MBPP_CROSSCHECK_TEMPLATE.format(
            aux_fn=ASSERTION_FN,
            inputs=inputs,
            ref_func=ref_func.replace(f" {entry_point}(", " ref_func("),
            entry_point=entry_point,
            atol=atol,
        )

    # default settings
    imports = set()
    aux_fn = ASSERTION_FN

    # inf exists in inputs/results
    if entry_point in ("zero_count", "minimum"):
        imports.add("from math import inf")

    test_code = MBPP_TEST_TEMPLATE.format(
        imports="\n".join(imports),
        aux_fn=aux_fn,
        inputs=inputs,
        results=results,
        entry_point=entry_point,
        atol=atol,
    )

    return task_id, test_code


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

    plus_problems = get_mbpp_plus(mini=False)
    dataset_hash = get_mbpp_plus_hash()

    original_mbpp = get_mbpp()

    compatible_problems = {}
    expected_outputs = get_groundtruth(
        plus_problems, dataset_hash, MBPP_OUTPUT_NOT_NONE_TASKS
    )

    # debugging: monitoring test code size
    id2bytes = {}

    n_workers = max(1, multiprocessing.cpu_count() // 4)
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = []
        for task_id, plus_form in tqdm(plus_problems.items()):
            # expected MBPP task_id is numbers directly
            # i.e., "666" instead of "Mbpp/666"
            # But in EvalPlus the task_id is "Mbpp/666"
            task_id_int = int(task_id.split("/")[-1])
            if args.debug_tasks and task_id_int not in args.debug_tasks:
                continue

            compatible_form = {
                "task_id": task_id_int,
                "code": plus_form["canonical_solution"],
                "prompt": original_mbpp[str(task_id_int)]["prompt"],
                "source_file": original_mbpp[str(task_id_int)]["source_file"],
                "test_imports": original_mbpp[str(task_id_int)]["test_imports"],
                "test_list": original_mbpp[str(task_id_int)]["test_list"],
            }
            compatible_problems[task_id_int] = compatible_form

            inputs = (
                plus_form["base_input"] + plus_form["plus_input"]
                if len(plus_form["plus_input"]) > 0
                else plus_form["base_input"]
            )
            results = (
                expected_outputs[task_id]["base"] + expected_outputs[task_id]["plus"]
            )

            inputs, results = deduplicate(inputs, results)

            assert len(inputs) == len(results)
            atol = plus_form["atol"]

            futures.append(
                executor.submit(
                    synthesize_test_code,
                    task_id_int,
                    plus_form["entry_point"],
                    inputs,
                    results,
                    compatible_form["code"],
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
            print('"""\n' + problem["prompt"] + '\n"""\n' + problem["code"])
            test_code = problem["test"]
            if True or len(test_code) <= 2048 + 512:
                print(test_code)
            else:
                print(problem["test"][:1024], "...")
                print("...", problem["test"][-1024:])
    else:
        with open(f"MbppPlus-OriginFmt-{MBPP_PLUS_VERSION}.jsonl", "w") as f:
            for problem in compatible_problems.values():
                f.write(json.dumps(problem) + "\n")


if __name__ == "__main__":
    main()

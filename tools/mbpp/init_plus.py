import json
import os
import pathlib
import shutil
from importlib import util
from inspect import getmembers, isfunction
from typing import Tuple

from tempdir import TempDir

from evalplus.data.mbpp import get_mbpp, mbpp_serialize_inputs

MBPP_PLUS_PATH = pathlib.Path(__file__).parent.parent.parent / "MbppBase.jsonl"

GROUNDTRUTH_MBPP_PATH = pathlib.Path(__file__).parent.parent.parent / "groundtruth/mbpp"


def _ret(entry_point) -> str:
    """
    This is a hacky function to return some garbages so that we can
    successfully run the function .
    """
    set_assertion_func = [
        "similar_elements",
        "find_char_long",
        "common_in_nested_lists",
        "extract_singly",
        "larg_nnum",
        "intersection_array",
        "k_smallest_pairs",
    ]
    if entry_point in set_assertion_func:
        return "()"
    return "1"


def get_entry_point(task_id: int, assertion: str) -> str:
    py_file_path = str(GROUNDTRUTH_MBPP_PATH) + f"/{str(task_id).zfill(3)}.py"
    spec = util.spec_from_file_location("inspect_module", py_file_path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    functions = [name for name, value in getmembers(module, isfunction)]

    # maybe exist some helper functions, filter them
    functions = [func for func in functions if func in assertion]
    if len(functions) > 1:
        print("more than one function: ", functions)

    return functions[0] if len(functions) > 0 else None


def get_code_and_contract_and_assertion(task_id: id) -> Tuple[str, str, str]:
    py_file_path = str(GROUNDTRUTH_MBPP_PATH) + f"/{str(task_id).zfill(3)}.py"
    with open(py_file_path) as reader:
        text = reader.read()
        # remove docstring
        start_index = text.find('"""')
        end_index = text.find('"""', start_index + 3)
        if start_index != -1 and end_index != -1:
            text = text[:start_index] + text[end_index + 3 :]

        lines = text.splitlines()
        assertion = ""
        contract = ""

        for i in range(len(lines)):
            if "$_CONTRACT_$" in lines[i]:
                contract += lines[i] + "\n"
            elif lines[i].startswith("assert"):
                assertion += lines[i] + "\n"

        for i in range(len(lines) - 1, -1, -1):
            if (
                "$_CONTRACT_$" in lines[i]
                or lines[i].startswith("assert")
                or lines[i] == ""
            ):
                del lines[i]

        for i in range(len(lines) - 1, -1, -1):
            if lines[i].startswith("import"):
                del lines[i]
            else:
                break

        code = "\n".join(lines)
        return "\n" + code + "\n", "\n" + contract, "\n" + assertion


def instrument_inputs(code, entry_point, test_code) -> str:
    globals()["_inputs"] = []
    fn_text = f"""{code.split(f"def {entry_point}")[0]}

def {entry_point}(*args):
    _inputs.append(args)
    return {_ret(entry_point)}
"""
    exec(fn_text + "\n" + test_code.replace("assert ", ""), globals())
    print(fn_text + "\n" + test_code.replace("assert ", ""))
    print(globals()["_inputs"])
    return globals()["_inputs"]


def get_atol(task_id: int) -> float:
    float_ans_list = [
        82,
        85,
        98,
        120,
        124,
        137,
        139,
        163,
        233,
        246,
        248,
        276,
        293,
        300,
        312,
        442,
        574,
        742,
        746,
    ]
    if task_id in float_ans_list:
        return 1e-4
    return 0


if __name__ == "__main__":
    assert not MBPP_PLUS_PATH.exists(), f"{MBPP_PLUS_PATH} already exists!"

    mbpp = get_mbpp()

    with TempDir() as temp_dir:
        tmp_file = os.path.join(temp_dir, MBPP_PLUS_PATH)
        with open(tmp_file, "w") as writer:
            for task in mbpp.values():
                task_id = int(task["task_id"])

                if task_id in [
                    163,
                    228,
                    304,
                    408,
                    776,
                    307,
                    417,
                    443,
                    444,
                    452,
                    464,
                    617,
                    627,
                    738,
                    747,
                    802,
                    393,
                    411,
                    584,
                    625,
                    756,
                    779,
                ]:
                    continue

                task["task_id"] = f"Mbpp/{task_id}"
                task["entry_point"] = get_entry_point(task_id, task["test_list"][0])
                task["prompt"] = f'"""\n{task["prompt"]}\n{task["test_list"][0]}\n"""\n'

                (
                    task["canonical_solution"],
                    task["contract"],
                    task["assertion"],
                ) = get_code_and_contract_and_assertion(task_id)
                if len(task["test_imports"]):
                    task["assertion"] = (
                        "\n".join(task["test_imports"]) + "\n" + task["assertion"]
                    )

                task["base_input"] = instrument_inputs(
                    task["canonical_solution"], task["entry_point"], task["assertion"]
                )

                task["atol"] = get_atol(task_id)

                del task["source_file"]
                del task["code"]
                del task["test_list"]
                del task["test_imports"]
                del task["assertion"]

                task["base_input"] = mbpp_serialize_inputs(task_id, task["base_input"])

                writer.write(json.dumps(task) + "\n")

        shutil.copy2(tmp_file, MBPP_PLUS_PATH)

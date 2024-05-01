import json
from typing import Callable, List


def check_id(data: dict, task_id: str):
    assert data[task_id]["task_id"] == f"HumanEval/{task_id}"


def evolve(src_file: str, tgt_file: str, fix: Callable):
    with open(src_file) as f:
        data = [json.loads(line) for line in f.readlines() if line]

    data = fix(data)
    with open(tgt_file, "wb") as f:
        for x in data:
            f.write((json.dumps(x) + "\n").encode("utf-8"))


def replay_contract(data: dict, tid: int) -> dict:
    code = data[tid]["prompt"] + data[tid]["contract"]
    exec(code)
    func = locals()[data[tid]["entry_point"]]

    new_inputs = []
    for inputs in data[tid]["plus_input"]:
        try:
            func(*inputs)
            new_inputs.append(inputs)
        except Exception as e:
            assert str(e) == "invalid inputs"

    before, after = len(data[tid]["plus_input"]), len(new_inputs)
    data[tid]["plus_input"] = new_inputs
    print(f"HumanEval/{tid}: {before} -> {after}")

    return before - after


def debug_output(version: str, tasks: List[int]):
    with open(f"HumanEvalPlus-{version}.jsonl") as f:
        data = [json.loads(line) for line in f.readlines() if line]

    data = {x["task_id"]: x for x in data}
    for tid in tasks:
        title = f"HumanEval/{tid}:\n"
        code = (
            data[f"HumanEval/{tid}"]["prompt"]
            + data[f"HumanEval/{tid}"]["contract"]
            + data[f"HumanEval/{tid}"]["canonical_solution"]
        )
        print(title)
        print(code)
        exec(code)
        print("====================================")

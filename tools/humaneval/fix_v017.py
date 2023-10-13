import math


def check_id(data, task_id):
    assert data[task_id]["task_id"] == f"HumanEval/{task_id}"


def fix(data):
    # https://github.com/evalplus/evalplus/issues/29
    check_id(data, 35)
    data[35]["contract"] += '    assert len(l) != 0, "invalid inputs" # $_CONTRACT_$\n'

    # https://github.com/evalplus/evalplus/issues/28
    check_id(data, 2)
    data[2][
        "contract"
    ] += '    assert number != float("+inf"), "invalid inputs" # $_CONTRACT_$\n'

    check_id(data, 99)
    data[99][
        "contract"
    ] += r"""    import math # $_CONTRACT_$
    assert not (math.isinf(value) or math.isnan(value)), "invalid inputs" # $_CONTRACT_$
"""
    # https://github.com/evalplus/evalplus/issues/27
    check_id(data, 1)
    data[1]["contract"] += '    assert cnt == 0, "invalid inputs" # $_CONTRACT_$\n'

    return data


if __name__ == "__main__":
    import json

    CONTRACT_INSPECT = [1, 2, 35, 99]
    SOURCE_VERSION = "v0.1.7"
    TARGET_VERSION = "v0.1.8"

    def evolve(src_file, tgt_file):
        with open(src_file) as f:
            data = [json.loads(line) for line in f.readlines() if line]

        data = fix(data)
        with open(tgt_file, "wb") as f:
            for x in data:
                f.write((json.dumps(x) + "\n").encode("utf-8"))

    evolve(
        f"HumanEvalPlus-{SOURCE_VERSION}.jsonl", f"HumanEvalPlus-{TARGET_VERSION}.jsonl"
    )
    evolve(
        f"HumanEvalPlus-Mini-{SOURCE_VERSION}.jsonl",
        f"HumanEvalPlus-Mini-{TARGET_VERSION}.jsonl",
    )

    # Debug the output of jsonl
    with open(f"HumanEvalPlus-{TARGET_VERSION}.jsonl") as f:
        data = [json.loads(line) for line in f.readlines() if line]

    data = {x["task_id"]: x for x in data}
    for tid in CONTRACT_INSPECT:
        print(data[f"HumanEval/{tid}"]["prompt"] + data[f"HumanEval/{tid}"]["contract"])
        print("====================================")

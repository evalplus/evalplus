import math


def check_id(data, task_id):
    assert data[task_id]["task_id"] == f"HumanEval/{task_id}"


def fix(data):
    # https://github.com/evalplus/evalplus/issues/44
    check_id(data, 115)
    data[115]["prompt"] = "import math\n" + data[115]["prompt"].replace(
        "    import math\n", ""
    )
    check_id(data, 114)
    data[114]["prompt"] = data[114]["prompt"].replace("import math\n", "")

    # https://github.com/evalplus/evalplus/issues/30#issue-1944054257
    check_id(data, 35)
    data[35][
        "contract"
    ] += '    assert all(type(x) in [int, float] for x in l), "invalid inputs" # $_CONTRACT_$\n'
    data[35]["canonical_solution"] = data[35]["canonical_solution"].replace(
        '    assert all(type(x) in [int, float] for x in l), "invalid inputs"\n', ""
    )

    # https://github.com/evalplus/evalplus/issues/30#issuecomment-1763502126
    check_id(data, 28)
    data[28][
        "contract"
    ] += '    assert isinstance(strings, list), "invalid inputs" # $_CONTRACT_$\n'

    # https://github.com/evalplus/evalplus/issues/34
    check_id(data, 32)
    terms = data[32]["contract"].splitlines()
    terms.insert(2, '    assert xs[-1] != 0, "invalid inputs" # $_CONTRACT_$')
    data[32]["contract"] = "\n".join(terms)

    # https://github.com/evalplus/evalplus/issues/35
    check_id(data, 160)
    terms = data[160]["contract"].splitlines()
    terms.insert(
        len(terms),
        '    assert not any([operand[i-1] == 0 and operator[i] == "//" for i in range(1, len(operand))]), "invalid inputs" # $_CONTRACT_$',
    )
    data[160]["contract"] = "\n".join(terms)

    return data


if __name__ == "__main__":
    import json

    TASK_INSPECT = [28, 32, 35, 114, 115, 160]
    SOURCE_VERSION = "v0.1.8"
    TARGET_VERSION = "v0.1.9"

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
    for tid in TASK_INSPECT:
        code = (
            data[f"HumanEval/{tid}"]["prompt"]
            + data[f"HumanEval/{tid}"]["contract"]
            + data[f"HumanEval/{tid}"]["canonical_solution"]
        )
        print(code)
        exec(code)
        print("====================================")

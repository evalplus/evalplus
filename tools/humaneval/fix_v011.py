def fix(data):
    # fix 140 https://github.com/evalplus/evalplus/issues/3
    assert data[140]["task_id"] == "HumanEval/140"
    data[140]["canonical_solution"] = data[140]["canonical_solution"].replace(
        "range(len(text)-1, 2, -1)", "range(len(text), 2, -1)"
    )

    # fix 75 https://github.com/evalplus/evalplus/issues/4
    assert data[75]["task_id"] == "HumanEval/75"
    org_contract = '\n    assert type(a) == int, "invalid inputs" # $_CONTRACT_$\n'
    assert org_contract in data[75]["contract"]
    data[75]["contract"] = (
        org_contract + '        assert a < 100, "invalid inputs" # $_CONTRACT_$\n'
    )
    data[75]["base_input"] = [x for x in data[75]["base_input"] if x[0] < 100]
    data[75]["plus_input"] = [x for x in data[75]["plus_input"] if x[0] < 100]

    # fix 129 https://github.com/evalplus/evalplus/issues/4
    assert data[129]["task_id"] == "HumanEval/129"
    data[129][
        "contract"
    ] = R"""
    assert type(k) == int, "invalid inputs" # $_CONTRACT_$
    assert k > 0, "invalid inputs" # $_CONTRACT_$
    assert len(grid) >= 2, "invalid inputs" # $_CONTRACT_$
    assert all(len(l) == len(grid) for l in grid), "invalid inputs" # $_CONTRACT_$
    assert {x for l in grid for x in l} == set(range(1, len(grid) ** 2 + 1)), "invalid inputs" # $_CONTRACT_$
"""

    def check_unique(grid):
        return {x for l in grid for x in l} == set(range(1, len(grid) ** 2 + 1))

    data[129]["base_input"] = [x for x in data[129]["base_input"] if check_unique(x[0])]
    data[129]["plus_input"] = [x for x in data[129]["plus_input"] if check_unique(x[0])]

    return data


if __name__ == "__main__":
    import json

    with open("HumanEvalPlus-v0.1.1.jsonl") as f:
        data = [json.loads(line) for line in f.readlines() if line]

    data = fix(data)
    with open("HumanEvalPlus-v0.1.2.jsonl", "wb") as f:
        for x in data:
            f.write((json.dumps(x) + "\n").encode("utf-8"))

    with open("HumanEvalPlus-Mini-v0.1.1.jsonl") as f:
        data = [json.loads(line) for line in f.readlines() if line]

    data = fix(data)
    with open("HumanEvalPlus-Mini-v0.1.2.jsonl", "wb") as f:
        for x in data:
            f.write((json.dumps(x) + "\n").encode("utf-8"))

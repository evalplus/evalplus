def check_id(data, task_id):
    assert data[task_id]["task_id"] == f"HumanEval/{task_id}"


def fix(data):
    # fix 53 https://github.com/evalplus/evalplus/issues/8
    check_id(data, 53)
    data[53]["contract"] = (
        '\n    assert isinstance(x, int), "invalid inputs" # $_CONTRACT_$'
        + '\n    assert isinstance(y, int), "invalid inputs" # $_CONTRACT_$\n'
    )
    data[53]["plus_input"] = [
        x
        for x in data[53]["plus_input"]
        if isinstance(x[0], int) and isinstance(x[1], int)
    ]

    # fix 0
    check_id(data, 0)
    data[0]["contract"] = (
        '\n    assert isinstance(threshold, float) and threshold > 0, "invalid inputs" # $_CONTRACT_$'
        + '\n    assert isinstance(numbers, list), "invalid inputs" # $_CONTRACT_$'
        + '\n    assert all([isinstance(v, (int, float)) for v in numbers]), "invalid inputs" # $_CONTRACT_$\n'
    )
    data[0]["plus_input"] = [
        x
        for x in data[0]["plus_input"]
        if isinstance(x[1], float) and x[1] > 0 and isinstance(x[0], list)
    ]

    # fix 3
    check_id(data, 3)
    data[3]["contract"] = (
        '\n    assert type(operations) == list, "invalid inputs" # $_CONTRACT_$'
        + '\n    assert all([isinstance(v, int) for v in operations]), "invalid inputs" # $_CONTRACT_$\n'
    )
    data[3]["plus_input"] = [x for x in data[3]["plus_input"] if isinstance(x[0], list)]

    # fix 9
    check_id(data, 9)
    data[9]["contract"] = (
        '\n    assert isinstance(numbers, list), "invalid inputs" # $_CONTRACT_$'
        + '\n    assert all([isinstance(v, int) for v in numbers]), "invalid inputs" # $_CONTRACT_$\n'
    )
    data[9]["plus_input"] = [x for x in data[9]["plus_input"] if isinstance(x[0], list)]

    # fix 148
    check_id(data, 148)
    data[148][
        "contract"
    ] = '\n    assert isinstance(planet1, str) and isinstance(planet2, str), "invalid inputs" # $_CONTRACT_$\n'
    data[148]["plus_input"] = [
        x
        for x in data[148]["plus_input"]
        if isinstance(x[0], str) and isinstance(x[1], str)
    ]

    # minor format fix 75
    check_id(data, 75)
    data[75]["contract"] = (
        '\n    assert type(a) == int, "invalid inputs" # $_CONTRACT_$'
        + '\n    assert a < 100, "invalid inputs" # $_CONTRACT_$\n'
    )

    return data


if __name__ == "__main__":
    import json

    with open("HumanEvalPlus-v0.1.2.jsonl") as f:
        data = [json.loads(line) for line in f.readlines() if line]

    data = fix(data)
    with open("HumanEvalPlus-v0.1.3.jsonl", "wb") as f:
        for x in data:
            f.write((json.dumps(x) + "\n").encode("utf-8"))

    with open("HumanEvalPlus-Mini-v0.1.2.jsonl") as f:
        data = [json.loads(line) for line in f.readlines() if line]

    data = fix(data)
    with open("HumanEvalPlus-Mini-v0.1.3.jsonl", "wb") as f:
        for x in data:
            f.write((json.dumps(x) + "\n").encode("utf-8"))

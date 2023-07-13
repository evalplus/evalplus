def check_id(data, task_id):
    assert data[task_id]["task_id"] == f"HumanEval/{task_id}"


def fix(data):
    check_id(data, 116)
    data[116]["contract"] = (
        '\n    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$'
        + '\n    assert all(isinstance(x, int) and x >= 0 for x in arr), "invalid inputs" # $_CONTRACT_$\n'
    )
    data[116]["plus_input"] = [
        l
        for l in data[116]["plus_input"]
        if isinstance(l[0], list) and all(isinstance(x, int) and x >= 0 for x in l[0])
    ]

    return data


if __name__ == "__main__":
    import json

    with open("HumanEvalPlus-v0.1.3.jsonl") as f:
        data = [json.loads(line) for line in f.readlines() if line]

    data = fix(data)
    with open("HumanEvalPlus-v0.1.4.jsonl", "wb") as f:
        for x in data:
            f.write((json.dumps(x) + "\n").encode("utf-8"))

    with open("HumanEvalPlus-Mini-v0.1.3.jsonl") as f:
        data = [json.loads(line) for line in f.readlines() if line]

    data = fix(data)
    with open("HumanEvalPlus-Mini-v0.1.4.jsonl", "wb") as f:
        for x in data:
            f.write((json.dumps(x) + "\n").encode("utf-8"))

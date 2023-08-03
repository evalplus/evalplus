def check_id(data, task_id):
    assert data[task_id]["task_id"] == f"HumanEval/{task_id}"


def check_valid(s: str):
    cnt = 0
    for ch in s:
        if ch == "(":
            cnt += 1
        elif ch == ")":
            cnt -= 1
        else:
            return False
        if cnt < 0:
            return False
    return cnt == 0


def fix(data):
    check_id(data, 6)

    data[6]["contract"] += '    assert cnt == 0, "invalid inputs"\n'
    data[6]["plus_input"] = [l for l in data[6]["plus_input"] if check_valid(l[0])]

    return data


if __name__ == "__main__":
    import json

    with open("HumanEvalPlus-v0.1.5.jsonl") as f:
        data = [json.loads(line) for line in f.readlines() if line]

    data = fix(data)

    with open("HumanEvalPlus-v0.1.6.jsonl", "wb") as f:
        for x in data:
            f.write((json.dumps(x) + "\n").encode("utf-8"))

    with open("HumanEvalPlus-Mini-v0.1.5.jsonl") as f:
        data = [json.loads(line) for line in f.readlines() if line]

    data = fix(data)
    with open("HumanEvalPlus-Mini-v0.1.6.jsonl", "wb") as f:
        for x in data:
            f.write((json.dumps(x) + "\n").encode("utf-8"))

import math


def check_id(data, task_id):
    assert data[task_id]["task_id"] == f"HumanEval/{task_id}"


def check_valid(op, num):
    try:
        exp = ""
        for i in range(len(op)):
            exp += str(num[i]) + str(op[i])
        exp += str(num[-1])
        exp = str(eval(exp))
    except:
        return False
    return True


def fix(data):
    check_id(data, 160)
    data[160]["plus_input"] = [
        l for l in data[160]["plus_input"] if check_valid(l[0], l[1])
    ]
    return data


if __name__ == "__main__":
    import json

    with open("HumanEvalPlus-v0.1.6.jsonl") as f:
        data = [json.loads(line) for line in f.readlines() if line]

    data = fix(data)

    with open("HumanEvalPlus-v0.1.7.jsonl", "wb") as f:
        for x in data:
            f.write((json.dumps(x) + "\n").encode("utf-8"))

    with open("HumanEvalPlus-Mini-v0.1.6.jsonl") as f:
        data = [json.loads(line) for line in f.readlines() if line]

    data = fix(data)
    with open("HumanEvalPlus-Mini-v0.1.7.jsonl", "wb") as f:
        for x in data:
            f.write((json.dumps(x) + "\n").encode("utf-8"))

import math


def check_id(data, task_id):
    assert data[task_id]["task_id"] == f"HumanEval/{task_id}"


def poly(xs, x):
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])


def check_valid(xs):
    if not (isinstance(xs, list) and len(xs) > 0 and len(xs) % 2 == 0):
        return False
    if not all(type(x) == int for x in xs):
        return False
    dxs = [xs[i] * i for i in range(1, len(xs))]

    def func(x):
        return poly(xs, x)

    def derivative(x):
        return poly(dxs, x)

    x, tol = 0, 1e-5
    for _ in range(1000):
        fx = func(x)
        dfx = derivative(x)
        if abs(fx) < tol:
            break
        x = x - fx / dfx
    if abs(poly(xs, x)) >= tol:
        return False
    return True


def fix(data):
    check_id(data, 32)
    data[32]["contract"] = (
        '\n    assert isinstance(xs, list) and len(xs) > 0 and len(xs) % 2 == 0, "invalid inputs" # $_CONTRACT_$'
        + '\n    assert all(type(x) == int for x in xs), "invalid inputs" # $_CONTRACT_$'
        + "\n    dxs = [xs[i] * i for i in range(1, len(xs))] # $_CONTRACT_$"
        + "\n    def func(x): # $_CONTRACT_$"
        + "\n        return poly(xs, x) # $_CONTRACT_$"
        + "\n    def derivative(x): # $_CONTRACT_$"
        + "\n        return poly(dxs, x) # $_CONTRACT_$"
        + "\n    x, tol = 0, 1e-5 # $_CONTRACT_$"
        + "\n    for _ in range(1000): # $_CONTRACT_$"
        + "\n        fx = func(x) # $_CONTRACT_$"
        + "\n        dfx = derivative(x) # $_CONTRACT_$"
        + "\n        if abs(fx) < tol: break # $_CONTRACT_$"
        + "\n        x = x - fx / dfx # $_CONTRACT_$"
        + '\n    assert abs(poly(xs, x)) < tol, "invalid inputs" # $_CONTRACT_$\n'
    )
    data[32]["plus_input"] = [l for l in data[32]["plus_input"] if check_valid(l[0])]

    return data


if __name__ == "__main__":
    import json

    with open("HumanEvalPlus-v0.1.4.jsonl") as f:
        data = [json.loads(line) for line in f.readlines() if line]

    data = fix(data)

    with open("HumanEvalPlus-v0.1.5.jsonl", "wb") as f:
        for x in data:
            f.write((json.dumps(x) + "\n").encode("utf-8"))

    with open("HumanEvalPlus-Mini-v0.1.4.jsonl") as f:
        data = [json.loads(line) for line in f.readlines() if line]

    data = fix(data)
    with open("HumanEvalPlus-Mini-v0.1.5.jsonl", "wb") as f:
        for x in data:
            f.write((json.dumps(x) + "\n").encode("utf-8"))

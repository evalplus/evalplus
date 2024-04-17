def check_id(data, n, task_id):
    assert data[n]["task_id"] == task_id


def fix(data):
    # fix: https://github.com/evalplus/evalplus/issues/156

    check_id(data, 334, "Mbpp/734")
    data[334]["prompt"] = data[334]["prompt"].replace(
        "https://www.geeksforgeeks.org/sum-of-products-of-all-possible-subarrays/", ""
    )

    check_id(data, 335, "Mbpp/735")
    data[335]["prompt"] = data[335]["prompt"].replace(
        "https://www.geeksforgeeks.org/toggle-bits-number-expect-first-last-bits/", ""
    )

    check_id(data, 336, "Mbpp/736")
    data[336]["prompt"] = data[336]["prompt"].replace(
        "https://www.w3resource.com/python-exercises/data-structures-and-algorithms/python-data-structure-exercise-24.php",
        "",
    )

    check_id(data, 338, "Mbpp/739")
    data[338]["prompt"] = data[338]["prompt"].replace(
        "https://www.geeksforgeeks.org/index-of-smallest-triangular-number-with-n-digits/",
        "",
    )

    check_id(data, 339, "Mbpp/740")
    data[339]["prompt"] = data[339]["prompt"].replace(
        "https://www.geeksforgeeks.org/python-convert-tuple-to-adjacent-pair-dictionary/",
        "",
    )

    check_id(data, 342, "Mbpp/743")
    data[342]["prompt"] = data[342]["prompt"].replace(
        "https://www.geeksforgeeks.org/python-program-right-rotate-list-n/", ""
    )

    check_id(data, 344, "Mbpp/745")
    data[344]["prompt"] = data[344]["prompt"].replace(
        "https://www.w3resource.com/python-exercises/lambda/python-lambda-exercise-24.php",
        "",
    )

    check_id(data, 347, "Mbpp/749")
    data[347]["prompt"] = data[347]["prompt"].replace(
        "https://www.geeksforgeeks.org/python-sort-numeric-strings-in-a-list/", ""
    )

    check_id(data, 349, "Mbpp/751")
    data[349]["prompt"] = data[349]["prompt"].replace(
        "https://www.geeksforgeeks.org/how-to-check-if-a-given-array-represents-a-binary-heap/",
        "",
    )

    check_id(data, 350, "Mbpp/752")
    data[350]["prompt"] = data[350]["prompt"].replace(
        "https://www.geeksforgeeks.org/jacobsthal-and-jacobsthal-lucas-numbers/", ""
    )

    check_id(data, 351, "Mbpp/753")
    data[351]["prompt"] = data[351]["prompt"].replace(
        "https://www.geeksforgeeks.org/python-find-minimum-k-records-from-tuple-list/",
        "",
    )

    check_id(data, 354, "Mbpp/757")
    data[354]["prompt"] = data[354]["prompt"].replace(
        "https://www.geeksforgeeks.org/python-program-to-count-the-pairs-of-reverse-strings/",
        "",
    )

    check_id(data, 359, "Mbpp/763")
    data[359]["prompt"] = data[359]["prompt"].replace(
        "https://www.geeksforgeeks.org/find-minimum-difference-pair/", ""
    )

    check_id(data, 366, "Mbpp/771")
    data[366]["prompt"] = data[366]["prompt"].replace(
        "https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-an-expression/",
        "",
    )

    check_id(data, 372, "Mbpp/780")
    data[372]["prompt"] = data[372]["prompt"].replace(
        "https://www.geeksforgeeks.org/python-combinations-of-sum-with-tuples-in-tuple-list/",
        "",
    )

    check_id(data, 373, "Mbpp/781")
    data[373]["prompt"] = data[373]["prompt"].replace(
        "https://www.w3resource.com/python-exercises/basic/python-basic-1-exercise-24.php",
        "",
    )

    check_id(data, 374, "Mbpp/782")
    data[374]["prompt"] = data[374]["prompt"].replace(
        "https://www.geeksforgeeks.org/sum-of-all-odd-length-subarrays/", ""
    )

    check_id(data, 392, "Mbpp/803")
    data[392]["prompt"] = data[392]["prompt"].replace(
        "https://www.geeksforgeeks.org/check-if-given-number-is-perfect-square-in-cpp/",
        "",
    )

    # fix: https://github.com/evalplus/evalplus/issues/147

    check_id(data, 375, "Mbpp/783")
    del data[375]

    check_id(data, 345, "Mbpp/746")
    del data[345]

    check_id(data, 318, "Mbpp/640")
    del data[318]

    check_id(data, 282, "Mbpp/595")
    del data[282]

    check_id(data, 270, "Mbpp/582")
    del data[270]

    check_id(data, 263, "Mbpp/574")
    del data[263]

    check_id(data, 231, "Mbpp/461")
    del data[231]

    check_id(data, 216, "Mbpp/442")
    del data[216]

    check_id(data, 212, "Mbpp/438")
    del data[212]

    check_id(data, 206, "Mbpp/431")
    del data[206]

    check_id(data, 187, "Mbpp/407")
    del data[187]

    check_id(data, 183, "Mbpp/400")
    del data[183]

    check_id(data, 180, "Mbpp/396")
    del data[180]

    check_id(data, 160, "Mbpp/295")
    del data[160]

    check_id(data, 121, "Mbpp/249")
    del data[121]

    check_id(data, 107, "Mbpp/229")
    del data[107]

    check_id(data, 94, "Mbpp/164")
    del data[94]

    check_id(data, 89, "Mbpp/143")
    del data[89]

    check_id(data, 67, "Mbpp/117")
    del data[67]

    check_id(data, 65, "Mbpp/115")
    del data[65]

    check_id(data, 37, "Mbpp/83")
    del data[37]

    return data


if __name__ == "__main__":
    import json

    TASK_INSPECT = [
        "Mbpp/734",
        "Mbpp/735",
        "Mbpp/736",
        "Mbpp/739",
        "Mbpp/740",
        "Mbpp/743",
        "Mbpp/745",
        "Mbpp/749",
        "Mbpp/751",
        "Mbpp/752",
        "Mbpp/753",
        "Mbpp/757",
        "Mbpp/763",
        "Mbpp/771",
        "Mbpp/780",
        "Mbpp/781",
        "Mbpp/782",
        "Mbpp/803",
    ]
    SOURCE_VERSION = "v0.1.0"
    TARGET_VERSION = "v0.2.0"

    def evolve(src_file, tgt_file):
        with open(src_file) as f:
            data = [json.loads(line) for line in f.readlines() if line]

        data = fix(data)
        with open(tgt_file, "wb") as f:
            for x in data:
                f.write((json.dumps(x) + "\n").encode("utf-8"))

    evolve(f"MbppPlus-{SOURCE_VERSION}.jsonl", f"MbppPlus-{TARGET_VERSION}.jsonl")

    # Inspect the output of jsonl
    with open(f"MbppPlus-{TARGET_VERSION}.jsonl") as f:
        data = [json.loads(line) for line in f.readlines() if line]

    data = {x["task_id"]: x for x in data}
    for task_id in TASK_INSPECT:
        print(data[task_id]["prompt"])
        print("====================================")

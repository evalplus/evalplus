def check_id(data, n, task_id):
    assert data[n]["task_id"] == task_id


def fix(data):
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

    SOURCE_VERSION = "v0.1.1"
    TARGET_VERSION = "v0.1.2"

    def evolve(src_file, tgt_file):
        with open(src_file) as f:
            data = [json.loads(line) for line in f.readlines() if line]

        data = fix(data)
        with open(tgt_file, "wb") as f:
            for x in data:
                f.write((json.dumps(x) + "\n").encode("utf-8"))

    evolve(f"MbppPlus-{SOURCE_VERSION}.jsonl", f"MbppPlus-{TARGET_VERSION}.jsonl")

from tools.humaneval.fix_utils import check_id, debug_output, evolve, replay_contract


def fix(data):
    # https://github.com/evalplus/evalplus/issues/180
    check_id(data, 1)
    replay_contract(data, 1)

    # https://github.com/evalplus/evalplus/issues/181
    check_id(data, 28)
    replay_contract(data, 28)

    # https://github.com/evalplus/evalplus/issues/182
    check_id(data, 99)
    data[99]["contract"] = data[99]["contract"].replace(
        "float(value)", "value = float(value)"
    )
    replay_contract(data, 99)

    # https://github.com/evalplus/evalplus/issues/185
    check_id(data, 160)
    data[160]["contract"] = data[160]["contract"].replace(
        'operand[i-1] == 0 and operator[i] == "//"',
        'operand[i] == 0 and operator[i-1] == "//"',
    )
    replay_contract(data, 160)

    return data


if __name__ == "__main__":
    TASK_INSPECT = [1, 28, 99, 160]
    SOURCE_VERSION = "v0.1.9"
    TARGET_VERSION = "v0.1.10"

    evolve(
        f"HumanEvalPlus-{SOURCE_VERSION}.jsonl",
        f"HumanEvalPlus-{TARGET_VERSION}.jsonl",
        fix,
    )
    evolve(
        f"HumanEvalPlus-Mini-{SOURCE_VERSION}.jsonl",
        f"HumanEvalPlus-Mini-{TARGET_VERSION}.jsonl",
        fix,
    )

    debug_output(TARGET_VERSION, TASK_INSPECT)

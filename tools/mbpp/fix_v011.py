def check_id(data, n, task_id):
    assert data[n]["task_id"] == task_id


def fix(data):
    # fix: https://github.com/evalplus/evalplus/issues/210

    check_id(data, 215, "Mbpp/459")
    data[215][
        "canonical_solution"
    ] = """
def remove_uppercase(str1):
  return ''.join(c for c in str1 if not c.isupper())
"""

    check_id(data, 55, "Mbpp/102")
    data[55][
        "canonical_solution"
    ] = """
def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])
"""

    check_id(data, 236, "Mbpp/559")
    data[236][
        "canonical_solution"
    ] = """
def max_sub_array_sum(arr, n):
    max_so_far = arr[0] if len(arr) else 0
    max_ending_here = arr[0] if len(arr) else 0
    for i in range(1, n):
        max_ending_here = max(arr[i], max_ending_here + arr[i])
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far
"""

    return data


if __name__ == "__main__":
    import json

    TASK_INSPECT = [
        "Mbpp/459",
        "Mbpp/102",
        "Mbpp/559",
    ]
    SOURCE_VERSION = "v0.2.0"
    TARGET_VERSION = "v0.2.1"

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
        print(data[task_id]["canonical_solution"])
        print("====================================")

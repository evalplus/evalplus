"""Repair Mbpp/287's integer oracle without changing its tests (issue #308)."""


def fix(data):
    tasks = [task for task in data if task["task_id"] == "Mbpp/287"]
    if len(tasks) != 1 or tasks[0]["entry_point"] != "square_Sum":
        raise ValueError(
            "Expected exactly one Mbpp/287 task with square_Sum entry point"
        )
    tasks[0][
        "canonical_solution"
    ] = """
def square_Sum(n):
    return 2 * n * (n + 1) * (2 * n + 1) // 3
"""
    return data


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    if args.source.resolve() == args.destination.resolve():
        parser.error("Source and destination must differ")
    with args.source.open() as source:
        data = [json.loads(line) for line in source if line.strip()]
    data = fix(data)
    # New output only: the official source/version is never overwritten.
    with args.destination.open("x") as destination:
        for task in data:
            destination.write(json.dumps(task) + "\n")

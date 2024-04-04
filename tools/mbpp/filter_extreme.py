if __name__ == "__main__":
    import json

    from evalplus.data.mbpp import MBPP_PLUS_VERSION, _ready_mbpp_plus_path
    from evalplus.data.utils import stream_jsonl

    # just load raw data
    plus_path = _ready_mbpp_plus_path()
    data = {task["task_id"]: task for task in stream_jsonl(plus_path)}
    # Process data
    for task_id, task in data.items():
        # =============================================================
        filtered_input = []
        if task["task_id"] == "Mbpp/239":
            # filter tests in data[task_id]["plus_inputs"]
            for m, n in data[task_id]["plus_input"]:
                if m < 100:
                    filtered_input.append((m, n))
            data[task_id]["plus_input"] = filtered_input
        elif task["task_id"] in ["Mbpp/274"]:
            for (n,) in data[task_id]["plus_input"]:
                if n < 25:
                    filtered_input.append((n,))
            data[task_id]["plus_input"] = filtered_input
        elif task["task_id"] == "Mbpp/392":
            for (n,) in data[task_id]["plus_input"]:
                # 20bit signed integer max
                if n <= 2 ** (20 - 1) - 1:
                    filtered_input.append((n,))
            data[task_id]["plus_input"] = filtered_input
        elif task["task_id"] in ["Mbpp/388", "Mbpp/599", "Mbpp/605", "Mbpp/781"]:
            for (n,) in data[task_id]["plus_input"]:
                # 27bit signed integer max
                if n <= 2 ** (27 - 1) - 1:
                    filtered_input.append((n,))
            data[task_id]["plus_input"] = filtered_input
        # =============================================================

    # Save outputs
    with open(f"MbppPlus-NoExtreme-{MBPP_PLUS_VERSION}.jsonl", "w") as f:
        for task in data.values():
            f.write(json.dumps(task) + "\n")

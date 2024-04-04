if __name__ == "__main__":
    import json

    from evalplus.data import get_human_eval_plus
    from evalplus.data.humaneval import HUMANEVAL_PLUS_VERSION

    data = get_human_eval_plus()

    # Process data
    for task_id, task in data.items():
        # =============================================================
        filtered_inputs = []
        if task["task_id"] in ["HumanEval/25", "HumanEval/77"]:
            # factorize(n), is_cube(n)
            # filter tests in data[task_id]["plus_inputs"]
            neg_threshold = -(2 ** (27 - 1))
            pos_threshold = 2 ** (27 - 1) - 1
            for (inp,) in task["plus_input"]:
                if neg_threshold <= inp <= pos_threshold:
                    filtered_inputs.append((inp,))
            data[task_id]["plus_input"] = filtered_inputs
        elif task["task_id"] == "HumanEval/39":
            # prime_fib(n)
            threshold = 11
            for (inp,) in task["plus_input"]:
                if inp <= threshold:
                    filtered_inputs.append((inp,))
            data[task_id]["plus_input"] = filtered_inputs
        elif task["task_id"] == "HumanEval/55":
            # fib(n)
            threshold = 40
            for (inp,) in task["plus_input"]:
                if inp <= threshold:
                    filtered_inputs.append((inp,))
            data[task_id]["plus_input"] = filtered_inputs
        elif task["task_id"] == "HumanEval/63":
            # fibfib(n)
            threshold = 30
            for (inp,) in task["plus_input"]:
                if inp <= threshold:
                    filtered_inputs.append((inp,))
            data[task_id]["plus_input"] = filtered_inputs
        elif task["task_id"] == "HumanEval/96":
            # is_prime(n)
            threshold = 1e4
            for (inp,) in task["plus_input"]:
                if inp <= threshold:
                    filtered_inputs.append((inp,))
            data[task_id]["plus_input"] = filtered_inputs
        elif task["task_id"] == "HumanEval/138":
            # is_equal_to_sum_even(n)
            threshold = 100
            for (inp,) in task["plus_input"]:
                if abs(inp) <= threshold:
                    filtered_inputs.append((inp,))
            data[task_id]["plus_input"] = filtered_inputs
        # =============================================================

    # Save outputs
    with open(f"HumanEvalPlus-NoExtreme-{HUMANEVAL_PLUS_VERSION}.jsonl", "w") as f:
        for task in data.values():
            f.write(json.dumps(task) + "\n")

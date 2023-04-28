if __name__ == "__main__":
    import argparse
    import json
    import os

    from tempdir import TempDir

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="humaneval", type=str)
    parser.add_argument("--plus-input", required=True, type=str)
    parser.add_argument("--output", required=True, type=str)
    args = parser.parse_args()

    assert args.dataset == "humaneval"
    assert not os.path.exists(args.output), f"{args.output} already exists!"

    with TempDir() as tempdir:
        # Generate inputs
        plus_input = {}
        with open(args.plus_input) as file:
            for line in file:
                problem = json.loads(line)
                plus_input[problem["task_id"]] = problem["inputs"]

        tempf = None
        if args.dataset == "humaneval":
            from evalplus.data import get_human_eval_plus

            # Allow it to be incomplete
            problems = get_human_eval_plus(err_incomplete=False)
            tempf = os.path.join(tempdir, "HumanEvalPlus.jsonl")
            with open(tempf, "w") as file:
                for problem in problems:
                    problem["plus_input"] = plus_input[problem["task_id"]]
                    file.write(json.dumps(problem) + "\n")

        # Move to the right place
        os.rename(tempf, args.output)

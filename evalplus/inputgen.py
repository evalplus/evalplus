"""Generate a .jsonl file where each line is a json object
representing a programming problem with a task ID ("task_id")
and a list of enhanced inputs ("inputs") for that task.
"""

import argparse
import json
import os

from evalplus.gen.chatgpt_gen import ChatGPTGen
from evalplus.gen.type_mut import TypedMutGen


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def input_generation(args, problems):
    with open(args.output, "w") as file:
        for problem in problems:
            new_input = {}
            task_id = problem["task_id"]
            print(f"generating inputs for {task_id} ...")
            # by default we do not include constraints in the prompt
            code = problem["prompt"] + problem["canonical_solution"]
            c_code = (
                problem["prompt"] + problem["contract"] + problem["canonical_solution"]
            )
            # first generate chatgpt
            input_gen = ChatGPTGen(
                problem["base_input"], problem["entry_point"], c_code, code
            ).generate(args.chatgpt_len)
            # generate mutation next
            input_gen.extend(
                TypedMutGen(input_gen, problem["entry_point"], c_code).generate(
                    args.mut_len
                )
            )
            print(f"generated {len(input_gen)} inputs")
            new_input["task_id"] = task_id
            new_input["inputs"] = input_gen
            file.write(json.dumps(new_input, cls=SetEncoder) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True, type=str)
    parser.add_argument("--chatgpt_len", required=True, type=int)
    parser.add_argument("--mut_len", required=True, type=int)
    parser.add_argument(
        "--output", default=None, type=int, help="Output .jsonl file name."
    )
    args = parser.parse_args()

    problems = None
    if args.dataset == "humaneval":
        from evalplus.data import get_human_eval_plus

        # Allow it to be incomplete
        problems = get_human_eval_plus(err_incomplete=False)
        if args.output is None:
            args.output = "HumanEvalPlusInputs.jsonl"

    if problems is None:
        raise NotImplementedError(f"Unsupported dataset: {args.dataset}")

    assert os.path.isfile(args.output), f"{args.output} already exists!"
    input_generation(args, problems)


if __name__ == "__main__":
    main()

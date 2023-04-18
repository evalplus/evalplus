import argparse
import json

from eval_plus.input_generation.chatgpt_gen import ChatGPTGen
from eval_plus.input_generation.mut_gen import MutateGen
from eval_plus.utils import HUMANEVAL_PLUS_INPUTS_PATH, get_human_eval_plus


def input_generation(args, problems):

    with open(HUMANEVAL_PLUS_INPUTS_PATH, "a") as file:
        for problem in problems:
            # cannot handle dicts yet.
            if "95" in problem["task_id"]:
                continue
            new_input = {}
            p_name = problem["task_id"].replace("/", "_")
            print(f"generating inputs for {p_name} ...")
            # by default we do not include constructs in the prompt
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
                MutateGen(input_gen, problem["entry_point"], c_code).generate(
                    args.mut_len
                )
            )
            print(f"generated {len(input_gen)} inputs")
            new_input["task_id"] = p_name
            new_input["inputs"] = input_gen
            file.write(json.dumps(new_input) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True, type=str)
    parser.add_argument("--chatgpt_len", required=True, type=int)
    parser.add_argument("--mut_len", required=True, type=int)
    args = parser.parse_args()
    if args.dataset not in ["humaneval"]:
        raise NotImplementedError("Unsupported dataset: {}".format(args.dataset))

    assert (
        not HUMANEVAL_PLUS_INPUTS_PATH.exists()
    ), f"{HUMANEVAL_PLUS_INPUTS_PATH} already exists!"
    problems = get_human_eval_plus()
    input_generation(args, problems)


if __name__ == "__main__":
    main()

"""Purpose of this file: Sanitize the code produced by LLMs for the following reasons.
1. Vicuna generated code could miss one white space. We fix the white space to make Vicuna more capable.
2. {Our fault lol.} We find more EOFs tokens afterwards and truncate some messy code afterwards.
"""

import os
from warnings import warn

from tqdm import tqdm

from evalplus.data import get_human_eval_plus, get_mbpp_plus
from tools.checker import syntax_check

INCODER_EXTRA = ["</code>", "<|", "</CODE>"]
POLYCODER_EXTRA = ["\n//", "\n/*"]
NON_CODE_EOFS = ["<|endoftext|>", "\n```", "\n</s>", "\n#"]


def get_all_python_files(folder):
    # return a list of full-path python files
    py_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files


def remove_unindented_lines(code, ok_starts):
    lines = code.splitlines()
    cut_idx = None
    for i, line in enumerate(lines):
        if any([line.startswith(t) for t in ok_starts]) or line.strip() == "":
            continue

        lspace = len(line) - len(line.lstrip())
        if lspace == 0:
            cut_idx = i
            break

    return "\n".join(lines[:cut_idx])


def to_four_space_indents(old_code):
    new_code = ""
    for line in old_code.splitlines():
        lspace = len(line) - len(line.lstrip())
        if lspace == 3:
            new_code += " "
        new_code += line + "\n"
    return new_code


if __name__ == "__main__":
    import argparse
    import pathlib

    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, required=True)
    parser.add_argument("--eof", action="store_true")
    parser.add_argument("--inplace", action="store_true")
    parser.add_argument(
        "--rm-prefix-lines", type=str, help="Remove lines starting with this"
    )
    parser.add_argument(
        "--dataset", required=True, type=str, choices=["humaneval", "mbpp"]
    )
    parser.add_argument(
        "--debug-task", type=str, help="Enter the task ID to only sanitize that task."
    )

    args = parser.parse_args()

    # task_id -> entry_point
    entry_point = {}
    prompts = {}

    if args.dataset == "humaneval":
        dataset = get_human_eval_plus()
    elif args.dataset == "mbpp":
        dataset = get_mbpp_plus()

    for task_id, problem in dataset.items():
        entry_point[task_id] = problem["entry_point"]
        prompts[task_id] = problem["prompt"]

    # make a new folder with "-sanitized" suffix
    old_folder = pathlib.Path(args.folder)
    if args.inplace:
        new_folder = old_folder
    else:
        new_folder = old_folder.parent / (old_folder.name + "-sanitized")

    nsan = 0
    ntotal = 0
    for pyf in tqdm(get_all_python_files(args.folder)):
        # Get [?] from "[prefix]/{HumanEval, Mbpp}_[?]/[number].py":
        task_id = pyf.split("/")[-2].replace("_", "/")
        if args.debug_task is not None and task_id != args.debug_task:
            continue

        ntotal += 1
        old_code = open(pyf).read()

        if args.rm_prefix_lines is not None:
            old_code = "\n".join(
                [
                    line
                    for line in old_code.splitlines()
                    if not line.startswith(args.rm_prefix_lines)
                ]
            )

        old_code = "\n" + old_code
        # basic handling of chat output
        for blk in ["\n```python\n", "\n```\n"]:
            old_code = old_code.split(blk, maxsplit=1)[-1].split("\n```", maxsplit=1)[0]
            old_code = "\n" + old_code

        def_left = "def " + entry_point[task_id]
        if def_left not in old_code:
            warn(f"Cannot find {def_left} in {pyf}. Skipping.")

        if args.dataset == "humaneval":
            imports, def_right = prompts[task_id].split(def_left)
            new_code = imports + def_left + old_code.split(def_left)[-1]
        elif args.dataset == "mbpp":
            new_code = old_code

        chunks = new_code.split(def_left)  # imports + def_left + {def_right + impl}

        new_code = def_left + def_left.join(chunks[1:])  # fn + impl

        if "chatgpt" in args.folder or "deepseek" in args.folder:
            tmp = ""
            for line in new_code.splitlines():
                if line.strip() == "python":
                    continue
                tmp += line + "\n"
            new_code = tmp

        new_code = to_four_space_indents(new_code)

        if args.eof:
            eof_strs = NON_CODE_EOFS
            if "incoder" in args.folder:
                eof_strs = eof_strs + INCODER_EXTRA
            if "polycoder" in args.folder:
                eof_strs = eof_strs + POLYCODER_EXTRA
            if "mistral" in args.folder:
                eof_strs = eof_strs + [r"</s>"]
            for eof in eof_strs:
                new_code = new_code.split(eof)[0]

        # remove lines that are not indented
        new_code = remove_unindented_lines(new_code, ["def "])
        new_code = chunks[0] + new_code

        # cut off the last function if it is incomplete
        last_fn = "def " + new_code.split("\ndef ")[-1]
        if not syntax_check(last_fn):
            new_code = "\ndef ".join(new_code.split("\ndef ")[:-1])

        # write to new folder
        new_pyf = pyf.replace(str(old_folder), str(new_folder))

        if new_code.strip() != old_code.strip():
            print("Sanitized: ", pyf, "->", new_pyf)
            nsan += 1

        pathlib.Path(new_pyf).parent.mkdir(parents=True, exist_ok=True)
        with open(new_pyf, "w") as f:
            f.write(new_code)

    print(f"Sanitized {nsan} out of {ntotal} files.")

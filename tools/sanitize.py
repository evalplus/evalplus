"""Purpose of this file: Sanitize the code produced by LLMs for the following reasons.
1. Vicuna generated code could miss one white space. We fix the white space to make Vicuna more capable.
2. {Our fault lol.} We find more EOFs tokens afterwards and truncate some messy code afterwards.
"""

import os

from tqdm import tqdm

from evalplus.data import get_human_eval_plus, get_mbpp_plus

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
    new_code = ""
    for line in code.splitlines():
        if any([line.startswith(t) for t in ok_starts]) or line.strip() == "":
            new_code += line + "\n"
            continue

        lspace = len(line) - len(line.lstrip())
        if lspace == 0:
            continue

        new_code += line + "\n"

    return new_code


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
        "--dataset", required=True, type=str, choices=["humaneval", "mbpp"]
    )

    args = parser.parse_args()

    # task_id -> entry_point
    entry_point = {}
    prompts = {}

    if args.dataset == "humaneval":
        dataset = get_human_eval_plus()
    elif args.dataset == "mbpp":
        dataset = get_mbpp_plus()
    else:
        raise NotImplementedError

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

        ntotal += 1
        old_code = open(pyf).read()

        def_left = "def " + entry_point[task_id] + "("
        if args.dataset == "humaneval":
            imports, def_right = prompts[task_id].split(def_left)
            new_code = imports + def_left + old_code.split(def_left)[-1]
        elif args.dataset == "mbpp":
            new_code = old_code

        chunks = new_code.split(def_left)  # imports + def_left + {def_right + impl}
        if len(chunks) == 2:
            new_code = def_left + chunks[-1]  # fn + impl

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
        ok_starts=[def_left]

        # some helper functions need to be kept
        if args.dataset == "mbpp":
            if def_left == "def count_Primes_nums(":
                ok_starts.append("def is_Prime(")
            elif def_left == "def heap_sort(":
                ok_starts.append("def heapify(")
        new_code = remove_unindented_lines(new_code, ok_starts)

        if len(chunks) == 2:
            new_code = chunks[0] + new_code

        # write to new folder
        new_pyf = pyf.replace(str(old_folder), str(new_folder))

        if new_code.strip() != old_code.strip():
            print("Sanitized: ", pyf, "->", new_pyf)
            nsan += 1

        pathlib.Path(new_pyf).parent.mkdir(parents=True, exist_ok=True)
        with open(new_pyf, "w") as f:
            f.write(new_code)

    print(f"Sanitized {nsan} out of {ntotal} files.")

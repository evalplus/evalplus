"""Purpose of this file: Sanitize the code produced by LLMs for the following reasons.
1. Vicuna generated code could miss one white space. We fix the white space to make Vicuna more capable.
2. {Our fault lol.} We find more EOFs tokens afterwards and truncate some messy code afterwards.
"""

import os

from tqdm import tqdm

from evalplus.data import get_human_eval

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


if __name__ == "__main__":
    import argparse
    import pathlib

    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, required=True)
    parser.add_argument("--eof", action="store_true")

    args = parser.parse_args()

    # task_id -> entry_point
    entry_point = {}
    for task_id, problem in get_human_eval().items():
        entry_point[task_id] = problem["entry_point"]

    # make a new folder with "-sanitized" suffix
    old_folder = pathlib.Path(args.folder)
    new_folder = old_folder.parent / (old_folder.name + "-sanitized")

    nsan = 0
    ntotal = 0
    for pyf in tqdm(get_all_python_files(args.folder)):
        # Get [?] from "[prefix]/HumanEval_[?]/[number].py":
        task_id = pyf.split("/")[-2].replace("HumanEval_", "HumanEval/")

        ntotal += 1
        old_code = open(pyf).read()

        fndef = "def " + entry_point[task_id] + "("
        new_code = old_code
        chunks = new_code.split(fndef)
        # prefix
        # impl
        if len(chunks) == 2:
            new_code = fndef + chunks[-1]  # fn + impl

        if "chatgpt" in args.folder:
            tmp = ""
            for line in new_code.splitlines():
                if line.strip() == "python":
                    continue
                tmp += line + "\n"
            new_code = tmp

        if "vicuna" in args.folder:
            tmp = ""
            for line in new_code.splitlines():
                lspace = len(line) - len(line.lstrip())
                if lspace == 3:
                    tmp += " "
                tmp += line + "\n"
            new_code = tmp

        if args.eof:
            eof_strs = NON_CODE_EOFS
            if "incoder" in args.folder:
                eof_strs = eof_strs + INCODER_EXTRA
            if "polycoder" in args.folder:
                eof_strs = eof_strs + POLYCODER_EXTRA
            for eof in eof_strs:
                new_code = new_code.split(eof)[0]

        # remove lines that are not indented
        new_code = remove_unindented_lines(new_code, ok_starts=[fndef])

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

"""Purpose of this file: Sanitize the code produced by LLMs for the following reasons.
1. Vicuna generated code could miss one white space. We fix the white space to make Vicuna more capable.
2. {Our fault lol.} We find more EOFs tokens afterwards and truncate some messy code afterwards.
"""

import os
import re

from tqdm import tqdm


def get_all_python_files(folder):
    # return a list of full-path python files
    py_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files


if __name__ == "__main__":
    import argparse
    import pathlib

    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, required=True)
    parser.add_argument("--vicuna", action="store_true")
    parser.add_argument("--eof", action="store_true")

    args = parser.parse_args()

    # make a new folder with "-sanitized" suffix
    old_folder = pathlib.Path(args.folder)
    new_folder = old_folder.parent / (old_folder.name + "-sanitized")

    for pyf in tqdm(get_all_python_files(args.folder)):
        old_code = open(pyf).read()
        new_code = old_code

        if args.vicuna:
            new_code = ""
            for line in old_code.splitlines():
                lspace = len(line) - len(line.lstrip())
                if lspace == 3:
                    new_code += " "
                new_code += line + "\n"
        if args.eof:
            pass

        if new_code != old_code:
            print("Sanitized: ", pyf)

        # write to new folder
        new_pyf = pyf.replace(str(old_folder), str(new_folder))
        pathlib.Path(new_pyf).parent.mkdir(parents=True, exist_ok=True)
        with open(new_pyf, "w") as f:
            f.write(new_code)

"""Purpose of this file: Sanitize the code produced by LLMs for the following reasons.
1. Vicuna generated code could miss one white space. We fix the white space to make Vicuna more capable.
2. {Our fault lol.} We find more EOFs tokens afterwards and truncate some messy code afterwards.
"""

import ast
import re
import traceback
from typing import List, Optional


def syntax_check(code, verbose=False):
    try:
        ast.parse(code)
        return True
    except (SyntaxError, MemoryError):
        if verbose:
            traceback.print_exc()
        return False


def remove_unindented_lines(code, protect_before, execeptions, trim_tails):
    lines = code.splitlines()
    cut_idx = []
    cut_enabled = False
    for i, line in enumerate(lines):
        if not cut_enabled and line.startswith(protect_before):
            cut_enabled = True
            continue
        if line.strip() == "":
            continue
        if any(line.startswith(e) for e in execeptions):
            continue

        lspace = len(line) - len(line.lstrip())
        if lspace == 0:
            cut_idx.append(i)

        if any(line.rstrip().startswith(t) for t in trim_tails):
            # cut off everything behind
            cut_idx.extend(list(range(i, len(lines))))
            break

    return "\n".join([line for i, line in enumerate(lines) if i not in cut_idx])


def to_four_space_indents(old_code):
    new_code = ""
    for line in old_code.splitlines():
        lspace = len(line) - len(line.lstrip())
        if lspace == 3:
            new_code += " "
        new_code += line + "\n"
    return new_code


def sanitize(
    old_code: str,
    entry_point: str,
    rm_prefix_lines: Optional[str] = None,
    eofs: List = None,
):
    new_code = old_code
    if rm_prefix_lines is not None:
        new_code = "\n".join(
            [
                line
                for line in old_code.splitlines()
                if not line.startswith(rm_prefix_lines)
            ]
        )

    new_code = "\n" + new_code
    def_left = "def " + entry_point

    # basic handling of chat output
    new_code = new_code.replace("\n```python\n", "\n```\n")
    for chunk in new_code.split("\n```\n"):
        if def_left in chunk:
            new_code = chunk
            break

    chunks = [chunk for chunk in re.split(f"{def_left}\s*\(", new_code)]
    # TODO: having return does not mean this is complete
    bodies = [chunk for chunk in chunks[1:] if "    return " in chunk.split("\ndef")[0]]
    def_left = def_left + "("
    new_code = def_left + def_left.join(bodies) if len(bodies) > 0 else ""  # fn + impl
    new_code = to_four_space_indents(new_code)

    for eof in eofs or []:
        new_code = new_code.split(eof)[0]

    # remove lines starting from the first unindented line after def_left
    new_code = remove_unindented_lines(
        new_code,
        protect_before=def_left,
        execeptions=["def ", "import ", "from "],
        trim_tails=['"""', "if", "print"],
    )
    new_code = chunks[0] + new_code

    # cut all functions that are not syntactically correct && not the entry point
    parts = new_code.split("\ndef ")
    includes = [parts[0]]
    for fn in new_code.split("\ndef ")[1:]:
        if (
            fn.strip().startswith(entry_point + " ")
            or fn.strip().startswith(entry_point + "(")
            or syntax_check("\ndef " + fn)
        ):
            includes.append(fn)
    new_code = "\ndef ".join(includes)
    return new_code.strip()

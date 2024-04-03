from typing import Optional

from tree_sitter_languages import get_language, get_parser

from evalplus.sanitize import syntax_check


def code_extract(text: str) -> str:
    """The goal is simple. Given a message of N lines, you want to find
    i and j such that the code between line i and j is valid python code.
    Note:
    1. Maximize |j - i| -- the extracted code should be as long as possible
    2. Use syntax_check to check if the code is valid python code
    """
    lines = text.split("\n")
    longest_line_pair = (0, 0)
    for i, line in enumerate(lines):
        pass  # TODO(@tom)


def sanitize(code: str, entrypoint: Optional[str] = None):
    """Clean the code into a self-contained code as much as possible.
    Some notes:
    1. Remove all non-code texts (like chat messages) -- See `code_extract`
    2. If there are multiple function sharing the same name, only keep the first one
    3. If entrypoint is provided, only keep the code that is reachable from the entrypoint

    Args:
        code (str): _description_
        entrypoint (str, optional): _description_. Defaults to None.
    """

    # 1. Get a pure code
    code = code_extract(code)

    # 2. Analyze the code using tree-sitter according to the following criteria:
    language = get_language("python")
    parser = get_parser("python")
    tree = parser.parse(bytes(code, "utf8"))
    # > Only keep: (i) import statements; (ii) functions; and (iii) classes. Trim things like assertions.
    # TODO: @tom

    # > Deduplicate functions: if there are multiple function using the same name, only keep the first one
    # TODO: @tom

    # > If entrypoint is provided, only keep the functions that is reachable from the entrypoint
    # NOTE: in Python if func B is defined after func A, A can still use B.
    # TODO: @tom

    # > Trim functions without return statement -- they are either incomplete or not needed
    # TODO: @tom

    # Useful links:
    # https://github.com/grantjenks/py-tree-sitter-languages
    # https://tree-sitter.github.io/tree-sitter/


if __name__ == "__main__":
    icode = r"""Following is the code snippet:
```python
import numpy as np
from numpy import sin, cos

def f(x):
    return np.tan(x)

def g(x):
    return cos(f(x))

def g(x):
    return sin(f(x))

assert g(0) == 1
```
"""
    assert (
        sanitize(icode)
        == r"""import numpy as np
from numpy import sin, cos

def f(x):
    return np.tan(x)

def g(x):
    return cos(f(x))"""
    )

    assert sanitize("") == ""
    assert sanitize("hello") == ""

    # Add more tests
    # TODO: @tom

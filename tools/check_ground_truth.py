"""This script checks:
1. Independence of "contract" and "reference" in groundtruth. (i.e., it should work without the "contract" part)
"""

import pathlib

from rich.progress import track

from eval_plus.utils import get_human_eval_plus

if __name__ == "__main__":
    human_eval_plus = get_human_eval_plus()

    for i, task in track(enumerate(human_eval_plus)):
        fname = (
            pathlib.Path(__file__).parent.parent
            / "groundtruth"
            / (str(i).zfill(3) + "_" + task["entry_point"] + ".py")
        )
        print(fname)
        code = open(fname, "r").read()
        if task["contract"]:
            code = code.replace(task["contract"], "\n")
        exec(code, globals())

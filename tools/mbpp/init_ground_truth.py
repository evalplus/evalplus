"""This script will initialize a folder of Python texts from MBPP.
Based on this we will add our contract and modified ground-truth.
"""

import os
import pathlib

from evalplus.data.mbpp import get_mbpp

if __name__ == "__main__":
    # check existance of ground truth folder
    GT_DIR = pathlib.Path(__file__).parent.parent.parent / "groundtruth" / "mbpp"

    assert not os.path.exists(
        GT_DIR
    ), "Ground truth folder already exists! If you want to reinitialize, delete the folder first."

    GT_DIR.parent.mkdir(exist_ok=True)
    GT_DIR.mkdir()

    mbpp = get_mbpp()

    newline = "\n"

    for tid, task in mbpp.items():
        incomplete = f'''"""
{task["prompt"]}
"""

{task["code"]}

{newline.join(task["test_imports"])}

{newline.join(task["test_list"])}
'''

        with open(
            os.path.join(GT_DIR, f"{tid.zfill(3)}.py"),
            "w",
        ) as f:
            f.write(incomplete)

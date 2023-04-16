import os
import pathlib

from eval_plus.utils import get_human_eval

if __name__ == "__main__":
    # check existance of ground truth folder
    GT_DIR = pathlib.Path(__file__).parent.parent / "groundtruth"

    assert not os.path.exists(
        GT_DIR
    ), "Ground truth folder already exists! If you want to reinitialize, delete the folder first."

    os.mkdir(GT_DIR)

    human_eval = get_human_eval()
    for i, task in enumerate(human_eval):
        incomplete = (
            task["prompt"]
            + "    pass"
            + "\n\n"
            + task["test"]
            + "\n"
            + f"check({task['entry_point']})"
        )
        with open(
            os.path.join(GT_DIR, f"{str(i).zfill(3)}_{task['entry_point']}.py"),
            "w",
        ) as f:
            f.write(incomplete)

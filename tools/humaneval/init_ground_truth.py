import os
import pathlib

from evalplus.data.humaneval import get_human_eval

if __name__ == "__main__":
    # check existance of ground truth folder
    GT_DIR = pathlib.Path(__file__).parent.parent / "groundtruth" / "humaneval"

    assert not os.path.exists(
        GT_DIR
    ), "Ground truth folder already exists! If you want to reinitialize, delete the folder first."

    os.mkdir(GT_DIR)

    human_eval = get_human_eval()
    for i, (task_id, task) in enumerate(human_eval.items()):
        incomplete = (
            task["prompt"]
            + task["canonical_solution"]
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

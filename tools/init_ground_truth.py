import os
import pathlib
import tempdir
import gzip
import json

import wget

if __name__ == "__main__":
    # check existance of ground truth folder
    GT_FOLDER = pathlib.Path(__file__).parent.parent / "groundtruth"
    if not GT_FOLDER.exists():
        os.mkdir(GT_FOLDER)

    # Install HumanEval dataset and parse as jsonl
    # https://github.com/openai/human-eval/blob/master/data/HumanEval.jsonl.gz
    HUMAN_EVAL_URL = (
        "https://github.com/openai/human-eval/raw/master/data/HumanEval.jsonl.gz"
    )
    with tempdir.TempDir() as tmpdir:
        human_eval_path = os.path.join(tmpdir, "HumanEval.jsonl.gz")
        wget.download(HUMAN_EVAL_URL, human_eval_path)

        with gzip.open(human_eval_path, "rb") as f:
            human_eval = f.read().decode("utf-8")

        human_eval = human_eval.split("\n")
        human_eval = [json.loads(line) for line in human_eval if line]
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
                os.path.join(GT_FOLDER, f"{str(i).zfill(3)}_{task['entry_point']}.py"),
                "w",
            ) as f:
                f.write(incomplete)

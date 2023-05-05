"""This script checks:
1. Independence of "contract" and "canonical_solution" in groundtruth. (i.e., it should work without the "contract" part)
"""

import multiprocessing as mp
import pathlib

from rich.progress import track

from evalplus.data import get_human_eval_plus

if __name__ == "__main__":
    human_eval_plus = get_human_eval_plus().values()

    for i, task in track(enumerate(human_eval_plus)):
        fname = (
            pathlib.Path(__file__).parent.parent
            / "groundtruth"
            / "humaneval"
            / (str(i).zfill(3) + "_" + task["entry_point"] + ".py")
        )
        print(fname)
        code = open(fname, "r").read()
        if task["contract"]:
            assert task["contract"] in code
            code = code.replace(task["contract"], "\n")

        # run the code in a subprocess
        p = mp.Process(target=exec, args=(code, globals()))
        p.start()
        p.join(timeout=2)
        assert not p.is_alive(), f"Timeout for {fname}!"
        p.terminate()
        p.join()
        assert p.exitcode == 0, f"Error for {fname}! {code}"

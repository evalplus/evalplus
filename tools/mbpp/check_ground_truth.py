"""Test through all ground truth files in groundtruth/mbpp."""

import pathlib

import multiprocess as mp
from rich.progress import track

if __name__ == "__main__":
    mbpp_work_dir = pathlib.Path(__file__).parent.parent.parent / "groundtruth" / "mbpp"
    assert mbpp_work_dir.exists(), f"{mbpp_work_dir} does not exist!"
    for file in track(mbpp_work_dir.glob("*.py")):
        print(file)
        code = file.read_text()

        # run the code in a subprocess
        p = mp.Process(target=exec, args=(code, globals()))
        p.start()
        p.join(timeout=5)
        assert not p.is_alive(), f"Timeout for {file}!"
        p.terminate()
        p.join()
        assert p.exitcode == 0, f"Error for {file}! {code}"

from evalplus.data.utils import load_solutions, write_directory

SOLUTION = "def f():\n    # \u2192 non-ASCII comment\n    return 1\n"


def test_solution_directory_roundtrip_is_utf8(tmp_path):
    write_directory(tmp_path, [{"task_id": "HumanEval/0", "solution": SOLUTION}])
    written = tmp_path / "HumanEval_0" / "0.py"
    assert written.read_text(encoding="utf-8") == SOLUTION

    (loaded,) = list(load_solutions(tmp_path))
    assert loaded["task_id"] == "HumanEval/0"
    assert loaded["solution"] == SOLUTION

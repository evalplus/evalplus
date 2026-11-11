import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.mbpp.fix_square_sum import fix


@pytest.fixture
def data():
    return [
        {"task_id": "Mbpp/other", "canonical_solution": "unchanged"},
        {
            "task_id": "Mbpp/287",
            "entry_point": "square_Sum",
            "canonical_solution": "def square_Sum(n): return 2*n*(n+1)*(2*n+1)/3",
            "prompt": "sum of squares of first n even natural numbers",
            "contract": "non-negative integer n",
            "base_input": [[2], [3], [4]],
            "plus_input": [[0], [1], [1000000]],
            "atol": 0,
        },
    ]


def test_changes_only_the_requested_canonical_solution(data):
    original = copy.deepcopy(data)
    repaired = fix(data)
    assert repaired[0] == original[0]
    for key in original[1]:
        if key != "canonical_solution":
            assert repaired[1][key] == original[1][key]
    assert fix(copy.deepcopy(repaired)) == repaired


@pytest.mark.parametrize("n", [0, 1, 2, 3, 4, 100, 999999, 1000000, 1000009])
def test_reference_agrees_with_direct_integer_summation(data, n):
    scope = {}
    exec(fix(data)[1]["canonical_solution"], scope)
    result = scope["square_Sum"](n)
    assert isinstance(result, int)
    assert result == sum(even * even for even in range(2, 2 * n + 1, 2))


@pytest.mark.parametrize("problem", ["missing", "duplicate", "wrong_entry_point"])
def test_refuses_unexpected_input(data, problem):
    if problem == "missing":
        data = data[:1]
    elif problem == "duplicate":
        data.append(copy.deepcopy(data[1]))
    else:
        data[1]["entry_point"] = "different_problem"
    original = copy.deepcopy(data)
    with pytest.raises(ValueError):
        fix(data)
    assert data == original


def test_cli_writes_new_dataset_and_preserves_source(data, tmp_path):
    script = Path(__file__).resolve().parents[1] / "tools/mbpp/fix_square_sum.py"
    source = tmp_path / "source.jsonl"
    destination = tmp_path / "fixed.jsonl"
    source.write_text("".join(json.dumps(task) + "\n" for task in data))
    original = source.read_bytes()
    subprocess.run(
        [sys.executable, str(script), str(source), str(destination)], check=True
    )
    assert source.read_bytes() == original
    assert [json.loads(line) for line in destination.read_text().splitlines()] == fix(
        data
    )
    result = subprocess.run(
        [sys.executable, str(script), str(source), str(source)], capture_output=True
    )
    assert result.returncode != 0
    assert source.read_bytes() == original
    result = subprocess.run(
        [sys.executable, str(script), str(source), str(destination)],
        capture_output=True,
    )
    assert result.returncode != 0

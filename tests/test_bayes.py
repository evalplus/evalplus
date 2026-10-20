import json
import math
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace

import numpy as np
import pytest

from evalplus.eval.bayes import estimate_bayes_at_n
from evalplus.evaluate import evaluate


@pytest.mark.parametrize(
    "correct, mean, variance",
    [([0, 2], 0.5, 3 / 160), ([1, 1], 0.5, 1 / 40), ([0], 0.25, 3 / 80)],
)
def test_exact_moments(correct, mean, variance):
    result = estimate_bayes_at_n([2] * len(correct), correct)
    assert result["mean"] == pytest.approx(mean)
    assert result["std"] == pytest.approx(math.sqrt(variance))


def test_one_trial_and_permutation():
    assert estimate_bayes_at_n([1], [1]) == pytest.approx(
        {"mean": 2 / 3, "std": math.sqrt(1 / 18)}
    )
    assert estimate_bayes_at_n([1], [0])["std"] > 0
    assert estimate_bayes_at_n(np.array([3, 3]), np.array([0, 2])) == (
        estimate_bayes_at_n([3, 3], [2, 0])
    )


@pytest.mark.parametrize(
    "total, correct",
    [
        ([], []),
        ([0], [0]),
        ([2, 3], [0, 1]),
        ([2], [3]),
        ([2], [-1]),
        ([2], [1.5]),
        ([2.0], [1]),
        ([2], [True]),
        ([2], []),
    ],
)
def test_invalid_counts(total, correct):
    with pytest.raises(ValueError, match="Bayes@N"):
        estimate_bayes_at_n(total, correct)


def write_cached(tmp_path):
    samples = tmp_path / "samples.jsonl"
    samples.write_text("")
    path = tmp_path / "samples.eval_results.json"
    results = {
        "hash": "fixture",
        "custom": {"keep": True},
        "pass_at_k": {"base": {"pass@1": 0.5}},
        "eval": {
            "HumanEval/0": [
                {"base_status": "fail", "plus_status": "pass"},
                {"base_status": "timeout", "plus_status": "fail"},
            ],
            "HumanEval/1": [
                {"base_status": "pass", "plus_status": "pass"},
                {"base_status": "pass", "plus_status": "fail"},
            ],
        },
    }
    path.write_text(json.dumps(results))
    return samples, path, results


def test_cached_cli_preserves_evidence_and_adds_both_regimes(tmp_path):
    samples, path, original = write_cached(tmp_path)
    run = subprocess.run(
        [
            sys.executable,
            "-m",
            "evalplus.evaluate",
            "--dataset",
            "humaneval",
            "--samples",
            str(samples),
            "--bayes_at_n",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Bayes@N" in run.stdout
    result = json.loads(path.read_text())
    posterior = result.pop("bayes_at_n")
    assert result == original
    assert posterior["base"] == pytest.approx({"mean": 0.5, "std": math.sqrt(3 / 160)})
    assert posterior["plus"] == pytest.approx(
        {"mean": 3 / 8, "std": math.sqrt(7 / 320)}
    )


def test_default_leaves_cached_file_unchanged(tmp_path):
    samples, path, _ = write_cached(tmp_path)
    original = path.read_bytes()
    evaluate("humaneval", str(samples))
    assert path.read_bytes() == original


def test_base_only_accepts_absent_plus_status(tmp_path):
    samples, path, results = write_cached(tmp_path)
    for row in results["eval"].values():
        for sample in row:
            sample["plus_status"] = None
    path.write_text(json.dumps(results))
    evaluate("humaneval", str(samples), base_only=True, bayes_at_n=True)
    assert set(json.loads(path.read_text())["bayes_at_n"]) == {"base"}


@pytest.mark.parametrize("bad", [None, "unknown", 1])
def test_missing_grade_rejected_without_modifying_cache(tmp_path, bad):
    samples, path, results = write_cached(tmp_path)
    results["eval"]["HumanEval/1"][0]["plus_status"] = bad
    path.write_text(json.dumps(results))
    before = path.read_bytes()
    with pytest.raises(ValueError, match="evaluated statuses"):
        evaluate("humaneval", str(samples), bayes_at_n=True)
    assert path.read_bytes() == before


def test_ragged_cache_rejected(tmp_path):
    samples, path, results = write_cached(tmp_path)
    results["eval"]["HumanEval/0"].pop()
    path.write_text(json.dumps(results))
    before = path.read_bytes()
    with pytest.raises(ValueError, match="same number"):
        evaluate("humaneval", str(samples), bayes_at_n=True)
    assert path.read_bytes() == before


def test_fresh_evaluation_saves_posterior(tmp_path, monkeypatch):
    import importlib

    module = importlib.import_module("evalplus.evaluate")
    problems = {
        task: {"task_id": task, "base_input": [], "plus_input": []}
        for task in ["HumanEval/0", "HumanEval/1"]
    }
    samples = tmp_path / "fresh.jsonl"
    samples.write_text(
        "\n".join(
            json.dumps({"task_id": task, "solution": status})
            for task, row in [
                ("HumanEval/0", ["fail", "fail"]),
                ("HumanEval/1", ["pass", "pass"]),
            ]
            for status in row
        )
    )

    def grade(
        dataset,
        completion_id,
        problem,
        solution,
        expected_output,
        base_only,
        fast_check,
        identifier,
        *args
    ):
        return {
            "task_id": problem["task_id"],
            "completion_id": completion_id,
            "solution": solution,
            "_identifier": identifier,
            "base": (solution, []),
            "plus": (solution, []),
        }

    monkeypatch.setattr(module, "get_human_eval_plus", lambda **kw: problems)
    monkeypatch.setattr(module, "get_human_eval_plus_hash", lambda **kw: "fixture")
    monkeypatch.setattr(module, "get_groundtruth", lambda *a: {t: {} for t in problems})
    monkeypatch.setattr(module, "check_correctness", grade)
    monkeypatch.setattr(module, "ProcessPoolExecutor", ThreadPoolExecutor)
    monkeypatch.setattr(
        module,
        "threading",
        SimpleNamespace(Thread=lambda **kw: SimpleNamespace(start=lambda: None)),
    )
    evaluate("humaneval", str(samples), parallel=1, bayes_at_n=True)
    result = json.loads((tmp_path / "fresh.eval_results.json").read_text())
    assert result["pass_at_k"]["base"]["pass@1"] == 0.5
    assert result["bayes_at_n"]["base"] == pytest.approx(
        {"mean": 0.5, "std": math.sqrt(3 / 160)}
    )
    assert result["bayes_at_n"]["plus"] == result["bayes_at_n"]["base"]

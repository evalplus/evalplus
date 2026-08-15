import numpy as np

from evalplus.eval import estimate_pass_at_k
from evalplus.report import compare, load_per_task, summarize


PASS = "pass"
FAIL = "fail"


def make_results(per_task):
    """Build an evalplus-style results dict from {task_id: [statuses]}."""
    return {
        "eval": {
            task_id: [
                {"base_status": b, "plus_status": p} for b, p in statuses
            ]
            for task_id, statuses in per_task.items()
        }
    }


def test_single_sample_pass1_equals_resolved():
    results = make_results(
        {"t1": [(PASS, PASS)], "t2": [(FAIL, FAIL)], "t3": [(PASS, FAIL)]}
    )
    s = summarize(load_per_task(results))
    assert s["pass1_base"] == 2 / 3
    assert s["resolved_base"] == 2 / 3
    assert s["pass1_plus"] == 1 / 3
    assert s["resolved_plus"] == 1 / 3


def test_multi_sample_semantics_are_distinct():
    # t1: 1/2 samples pass -> pass@1 = 0.5, but resolved = 1.0
    results = make_results(
        {
            "t1": [(PASS, PASS), (FAIL, FAIL)],
            "t2": [(FAIL, FAIL), (FAIL, FAIL)],
        }
    )
    per_task = load_per_task(results)
    s = summarize(per_task)
    assert s["pass1_base"] == 0.25
    assert s["resolved_base"] == 0.5
    assert s["samples_per_task_min"] == 2
    assert s["samples_per_task_max"] == 2


def test_pass1_matches_upstream_estimator():
    results = make_results(
        {
            "t1": [(PASS, PASS), (FAIL, FAIL), (FAIL, FAIL)],
            "t2": [(PASS, PASS), (PASS, FAIL)],
        }
    )
    per_task = load_per_task(results)
    total = np.array([3, 2])
    base_c = np.array([1, 2])
    expected = float(estimate_pass_at_k(total, base_c, 1).mean())
    s = summarize(per_task)
    assert abs(s["pass1_base"] - expected) < 1e-12


def test_compare_detects_unmatched_sample_counts():
    a = make_results(
        {"t1": [(PASS, PASS)], "t2": [(PASS, PASS)], "t3": [(FAIL, FAIL)]}
    )
    b = make_results(
        {
            "t1": [(PASS, PASS), (PASS, PASS)],
            "t2": [(PASS, PASS)],
            "t3": [(FAIL, FAIL)],
        }
    )
    c = compare(load_per_task(a), load_per_task(b))
    assert c["sample_count_mismatches"] == ["t1"]
    assert c["shared"] == 3

    d = make_results(
        {"t1": [(PASS, PASS)], "t2": [(PASS, PASS)], "t3": [(FAIL, FAIL)]}
    )
    e = compare(load_per_task(a), load_per_task(d))
    assert e["sample_count_mismatches"] == []


def test_compare_counts_and_p():
    a = make_results(
        {"t1": [(PASS, PASS)], "t2": [(PASS, PASS)], "t3": [(FAIL, FAIL)]}
    )
    b = make_results(
        {"t1": [(PASS, PASS)], "t2": [(FAIL, FAIL)], "t3": [(PASS, PASS)]}
    )
    c = compare(load_per_task(a), load_per_task(b))
    assert c["shared"] == 3
    assert c["both"] == 1
    assert c["a_only"] == 1
    assert c["b_only"] == 1
    assert abs(c["p"] - 1.0) < 1e-12

"""Summarization of ``eval_results.json`` for honest leaderboard reporting.

Separates two metrics that are often conflated:

* ``pass@1`` — the standard EvalPlus estimator (``estimate_pass_at_k`` with
  ``k=1``), averaged over tasks exactly as ``evalplus.evaluate`` reports it;
* ``resolved`` — the per-task binary outcome "at least one sample passed",
  which is the convention used by SWE-bench-style paired comparisons and the
  metric on which the Wilson confidence interval is computed.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

from evalplus.eval import PASS, estimate_pass_at_k
from evalplus.uncertainty import paired_mcnemar, wilson_ci

SampleOutcome = Tuple[bool, bool]  # (base_ok, plus_ok)


def load_per_task(results: dict) -> Dict[str, List[SampleOutcome]]:
    """Return {task_id: [(base_ok, plus_ok), ...]} from an evalplus result dict."""
    per_task = {}
    for task_id, samples in results.get("eval", {}).items():
        per_task[task_id] = [
            (
                s.get("base_status") == PASS,
                s.get("base_status") == PASS and s.get("plus_status") == PASS,
            )
            for s in samples
        ]
    return per_task


def summarize(per_task: Dict[str, List[SampleOutcome]]) -> dict:
    """Aggregate pass@1 (upstream semantics) and per-task resolved rates."""
    n_tasks = len(per_task)
    if n_tasks == 0:
        raise ValueError("no tasks in results")
    total = np.array([len(s) for s in per_task.values()])
    base_c = np.array([sum(1 for ok, _ in s if ok) for s in per_task.values()])
    plus_c = np.array([sum(1 for _, ok in s if ok) for s in per_task.values()])
    resolved_base = np.array([any(ok for ok, _ in s) for s in per_task.values()])
    resolved_plus = np.array([any(ok for _, ok in s) for s in per_task.values()])

    pass1_base = float(estimate_pass_at_k(total, base_c, 1).mean())
    pass1_plus = float(estimate_pass_at_k(total, plus_c, 1).mean())
    r_base = int(resolved_base.sum())
    r_plus = int(resolved_plus.sum())
    lo_b, hi_b = wilson_ci(r_base, n_tasks)
    lo_p, hi_p = wilson_ci(r_plus, n_tasks)

    return {
        "tasks": n_tasks,
        "samples_per_task_min": int(total.min()),
        "samples_per_task_max": int(total.max()),
        "pass1_base": pass1_base,
        "pass1_plus": pass1_plus,
        "resolved_base": r_base / n_tasks,
        "resolved_base_ci": (lo_b, hi_b),
        "resolved_plus": r_plus / n_tasks,
        "resolved_plus_ci": (lo_p, hi_p),
    }


def compare(
    per_task_a: Dict[str, List[SampleOutcome]],
    per_task_b: Dict[str, List[SampleOutcome]],
) -> dict:
    """Exact paired McNemar on per-task resolved (base) outcomes."""
    resolved_a = {t: any(ok for ok, _ in s) for t, s in per_task_a.items()}
    resolved_b = {t: any(ok for ok, _ in s) for t, s in per_task_b.items()}
    shared = [t for t in resolved_a if t in resolved_b]
    if not shared:
        raise ValueError("no shared tasks between the two result files")
    both = sum(1 for t in shared if resolved_a[t] and resolved_b[t])
    a_only = sum(1 for t in shared if resolved_a[t] and not resolved_b[t])
    b_only = sum(1 for t in shared if resolved_b[t] and not resolved_a[t])
    return {
        "shared": len(shared),
        "both": both,
        "a_only": a_only,
        "b_only": b_only,
        "p": paired_mcnemar(a_only, b_only),
    }

"""Report pass@1 and per-task resolved rates with 95% Wilson CIs.

Reads an EvalPlus ``eval_results.json`` (as written by ``evalplus.evaluate``)
and prints:

* ``pass@1`` (base and plus) — the standard EvalPlus estimator, averaged over
  tasks exactly as upstream reports it;
* ``resolved`` (base and plus) — the per-task binary "at least one sample
  passed" rate, with a 95% Wilson score interval.

With ``--compare``, runs an exact paired McNemar test between two result
files on their shared task set, using the per-task resolved (base) outcomes.

A paired comparison is only valid under matched measurement conditions, so
``--compare`` aborts by default when any shared task has a different sample
count in the two files (e.g. 1 trial per task vs. 10 trials per task would
give the 10-trial run ten chances to resolve a task as passed). Pass
``--allow-unmatched-samples`` to compare anyway.

Examples::

    python tools/ci_report.py --results path/to/eval_results.json
    python tools/ci_report.py --results model_a.json --compare model_b.json
"""

import argparse
import json

from evalplus.report import compare, load_per_task, summarize


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", required=True, help="eval_results.json")
    parser.add_argument("--compare", help="second eval_results.json for McNemar")
    parser.add_argument(
        "--allow-unmatched-samples",
        action="store_true",
        help="compare even if shared tasks have different per-task sample counts",
    )
    args = parser.parse_args()

    with open(args.results, encoding="utf-8") as f:
        results = json.load(f)
    per_task = load_per_task(results)
    s = summarize(per_task)

    print(f"tasks: {s['tasks']}  (samples/task: "
          f"{s['samples_per_task_min']}-{s['samples_per_task_max']})")
    lo, hi = s["resolved_base_ci"]
    print(f"pass@1 (base): {s['pass1_base']:.4f}")
    print(f"resolved (base): {s['resolved_base']:.4f}  "
          f"95% CI [{lo:.4f}, {hi:.4f}]")
    lo, hi = s["resolved_plus_ci"]
    print(f"pass@1 (plus): {s['pass1_plus']:.4f}")
    print(f"resolved (plus): {s['resolved_plus']:.4f}  "
          f"95% CI [{lo:.4f}, {hi:.4f}]")

    if args.compare:
        with open(args.compare, encoding="utf-8") as f:
            other = json.load(f)
        other_per_task = load_per_task(other)
        c = compare(per_task, other_per_task)
        if c["sample_count_mismatches"] and not args.allow_unmatched_samples:
            shown = ", ".join(c["sample_count_mismatches"][:5])
            raise SystemExit(
                f"error: {len(c['sample_count_mismatches'])} shared task(s) "
                f"have different per-task sample counts ({shown}"
                f"{', ...' if len(c['sample_count_mismatches']) > 5 else ''}); "
                "the measurement conditions are not paired. Re-run with "
                "--allow-unmatched-samples to compare anyway."
            )
        print(f"paired comparison on {c['shared']} shared tasks "
              f"(resolved base): both {c['both']} | A-only {c['a_only']} | "
              f"B-only {c['b_only']} | McNemar p {c['p']:.4f}")


if __name__ == "__main__":
    main()

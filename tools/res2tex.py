"""Convert the results to an ingredient for LaTeX table.
"""

import argparse
import json
import os

import numpy as np
from termcolor import cprint

from eval_plus.evaluation.evaluate import estimate_pass_at_k


def analyze_resfile(resfile):
    before_summary = {}
    after_summary = {}

    res = json.load(open(resfile))["eval"]
    total = []
    before_pass = []
    after_pass = []
    for v in res.values():
        total.append(len(v["files"]))
        bc = sum([r[0] == SUCCESS for r in v["base"]])
        before_pass.append(bc)
        if v["plus"]:
            after_pass.append(
                sum(
                    [
                        v["plus"][i][0] == v["base"][i][0] == SUCCESS
                        for i in range(len(v["plus"]))
                    ]
                )
            )

    total = np.array(total)
    before_pass = np.array(before_pass)
    after_pass = np.array(after_pass)
    for k in [1, 10, 100]:
        if total.min() >= k:
            pass_at_k = estimate_pass_at_k(total, before_pass, k).mean()
            before_summary[f"pass@{k}"] = pass_at_k
    for k in [1, 10, 100]:
        if total.min() >= k:
            pass_at_k = estimate_pass_at_k(total, after_pass, k).mean()
            after_summary[f"pass@{k}"] = pass_at_k

    return before_summary, after_summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, required=True)
    args = parser.parse_args()

    # Analyszing 0.2~0.8 temperatures.
    resfiles = []
    TEMPS = [0.2, 0.4, 0.6, 0.8]
    # check existance
    for t in TEMPS:
        f = os.path.join(f"{args.type}_temp_{t}", f"eval_results.json")
        assert os.path.exists(f), f"{f} not found"
        resfiles.append(f)

    before_summary = {}
    after_summary = {}

    SUCCESS = "success"

    for resfile in resfiles:
        # load the results
        before, after = analyze_resfile(resfile)
        for k, v in before.items():
            before_summary.setdefault(k, []).append(v)
        for k, v in after.items():
            after_summary.setdefault(k, []).append(v)

    # print pass@1~100, and corresponding max temperature
    print("Before")
    print(before_summary)
    print("After")
    print(after_summary)

    # Analyszing greedy decoding (temperature=0.0)
    gf = os.path.join(f"{args.type}_temp_0.0", f"eval_results.json")
    assert os.path.exists(gf)
    bfgreedy, afgreedy = analyze_resfile(gf)
    bfgreedy = bfgreedy["pass@1"] * 100
    afgreedy = afgreedy["pass@1"] * 100

    TEXTTEMPS = [r"\temptwo{}", r"\tempfour{}", r"\tempsix{}", r"\tempeight{}"]

    def aplus(s) -> str:
        return r"\aplus{" + s + r"}"

    def make_line(summary, amax, ap=False):
        pkvals = [f"{100 * v[amax[i]]:.1f}" for i, v in enumerate(summary.values())]
        if ap:
            pkvals = [aplus(v) for v in pkvals]
        return (
            " & ".join(pkvals)
            + " & "
            + " & ".join([f"{TEXTTEMPS[i]}".replace("0.", ".") for i in amax])
            + r" \\"
        )

    print("LaTeX Table Ingredent")
    argmax = [np.argmax(v) for v in before_summary.values()]
    cprint(
        f"before & {bfgreedy:.1f} & " + make_line(before_summary, argmax),
        "green",
    )
    argmax = [np.argmax(v) for v in after_summary.values()]
    cprint(
        aplus("after")
        + f" & {aplus(f'{afgreedy:.1f}')} & "
        + make_line(after_summary, argmax, ap=True),
        "green",
    )

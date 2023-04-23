"""Convert the results to an ingredient for LaTeX table.
"""

import argparse
import json
import os

import numpy as np
from termcolor import cprint

from eval_plus.evaluation.evaluate import estimate_pass_at_k

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, required=True)
    args = parser.parse_args()

    resfiles = []
    TEMPS = [0.2, 0.4, 0.6, 0.8]
    # check existance
    for t in TEMPS:
        f = os.path.join(f"{args.type}_temp_{t}", f"eval_results.json")
        assert os.path.exists(f)
        resfiles.append(f)

    before_summary = {}
    after_summary = {}

    SUCCESS = "success"

    for resfile in resfiles:
        # load the results
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
            if (total >= k).all():
                pass_at_k = estimate_pass_at_k(total, before_pass, k).mean()
                before_summary.setdefault(f"pass@{k}", []).append(pass_at_k)
        for k in [1, 10, 100]:
            if (total >= k).all():
                pass_at_k = estimate_pass_at_k(total, after_pass, k).mean()
                after_summary.setdefault(f"pass@{k}", []).append(pass_at_k)

    # print pass@1~100, and corresponding max temperature
    print("Before")
    print(before_summary)
    print("After")
    print(after_summary)

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
    cprint("before & " + make_line(before_summary, argmax), "green")
    argmax = [np.argmax(v) for v in after_summary.values()]
    cprint(aplus("after") + " & " + make_line(after_summary, argmax, ap=True), "green")

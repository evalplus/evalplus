import collections
import json
import os

import matplotlib.pyplot as plt
import numpy as np

SMALL_SIZE = 10
MEDIUM_SIZE = 14
BIGGER_SIZE = 18

plt.rc("font", size=SMALL_SIZE)  # controls default text sizes
plt.rc("axes", titlesize=MEDIUM_SIZE)  # fontsize of the axes title
plt.rc("axes", labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc("xtick", labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
plt.rc("ytick", labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
plt.rc("legend", fontsize=MEDIUM_SIZE - 1)  # legend fontsize
plt.rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title

MIN_FAC_TWO = None
MIN_FAC = None

plt.rc("text", usetex=True)
# plt.rc("text.latex", preamble=r"\usepackage{xfrac}")

MODELS = [
    "codegen-2b",
    "codegen-6b",
    "codegen-16b",
    "vicuna-13b",
    "incoder-1b"
    # ADD MORE
]

TEMP = [0.2, 0.4, 0.6, 0.8]


def main():
    base_total = [0 for x in range(0, 164)]
    base_correct = [0 for x in range(0, 164)]
    new_correct = [0 for x in range(0, 164)]
    for model in MODELS:
        for temp in TEMP:
            result_path = os.path.join(
                "/JawTitan/EvalPlus/humaneval", f"{model}_temp_{temp}/eval_results.json"
            )
            assert os.path.isfile(result_path)
            with open(result_path, "r") as f:
                results = json.load(f)

            base_total = [
                sum(x)
                for x in zip(
                    base_total,
                    [len(x["base_files"]) for _, x in results["eval"].items()],
                )
            ]
            base_correct = [
                sum(x)
                for x in zip(
                    base_correct,
                    [
                        len(x["correct_files"])
                        for _, x in dict(sorted(results["eval"].items())).items()
                    ],
                )
            ]
            new_correct = [
                sum(x)
                for x in zip(
                    new_correct,
                    [
                        len(x["ncorrect_files"])
                        for _, x in dict(sorted(results["eval"].items())).items()
                    ],
                )
            ]

    x, y = [], []

    for b, n, t in zip(base_correct, new_correct, base_total):
        if b < 50:
            continue
        x.append(b / t)
        y.append(1 - (n / b))

    # plt.hist(base_correct, label='original', alpha=0.5, bins=50)
    # plt.hist(new_correct, label='new', alpha=0.5, bins=50)
    plt.scatter(y, x, alpha=0.5, s=100)
    plt.xlabel("reduction in successful code (after HumanEval+)")
    plt.ylabel("rate of successful code (using base HumanEval)")
    plt.savefig("temp.png", dpi=1000)


if __name__ == "__main__":
    main()

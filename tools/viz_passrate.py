import json
import os
import pickle
from os import PathLike
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

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

plt.rc("text", usetex=True)

SUCCESS = "success"


def get_data(paths: List[PathLike]):
    task2rate_old = None
    task2rate_new = None

    for path in tqdm(paths):  # each experiment
        res = json.load(open(path, "r"))["eval"]
        ntask = len(res)

        assert ntask == 164

        if task2rate_old is None and task2rate_new is None:
            task2rate_old = [[] for _ in range(ntask)]
            task2rate_new = [[] for _ in range(ntask)]
            # i-th => task-i pass rate for an experiment

        for i, v in enumerate(res.values()):  # each task
            base = v["base"]
            plus = v["plus"]
            bbv = np.array([s == SUCCESS for s, _ in base])
            pbv = np.array([s == SUCCESS for s, _ in plus])
            old_rate = np.mean(bbv)
            new_rate = np.mean(pbv & bbv)
            assert old_rate >= new_rate

            task2rate_old[i].append(old_rate)
            task2rate_new[i].append(new_rate)

    assert len(task2rate_old) == len(task2rate_new)
    return task2rate_old, task2rate_new


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=str, default="/JawTitan/EvalPlus/humaneval")
    args = parser.parse_args()

    paths = []
    for path in os.listdir(args.root):
        eval_json_path = os.path.join(args.root, path, "eval_results.json")
        if not os.path.isfile(eval_json_path) or not path[-1].isdigit():
            print(f"skip {path}")
            continue
        paths.append(eval_json_path)

    CACHE_PATH = "passrate.pkl"
    if os.path.isfile(CACHE_PATH):
        rate_old, rate_new = pickle.load(open(CACHE_PATH, "rb"))
    else:
        # cache
        rate_old, rate_new = get_data(paths)
        pickle.dump((rate_old, rate_new), open(CACHE_PATH, "wb"))

    for i, (rs_old, rs_new) in enumerate(zip(rate_old[47], rate_new[47])):
        print(paths[i])
        print(rs_old, rs_new)

    # scale to 100
    rate_old = [np.mean(rs) * 100 for rs in rate_old]
    rate_new = [np.mean(rs) * 100 for rs in rate_new]

    ntask = len(rate_old)

    # sort by old pass rate
    # numpy argsort
    indices = np.array(rate_old).argsort()
    # find unsolved tasks. i.e., indices where rate_old == 0
    unsolved = np.where(np.array(rate_old) == 0)[0]
    print("Unsolvable: ", unsolved)
    # sort indices according to the differences between rate_old and rate_new
    diff_indices = (np.array(rate_old) - np.array(rate_new)).argsort()
    for i in reversed(diff_indices[-10:]):
        print(
            f"#{i} drops {rate_old[i] - rate_new[i] :.1f}: {rate_old[i]:.1f} -> {rate_new[i]:.1f}"
        )

    rate_old = np.array(rate_old)[indices]
    rate_new = np.array(rate_new)[indices]
    # rate_old, rate_new = zip(*sorted(zip(rate_old, rate_new), key=lambda x: x[0]))

    # making a barplot
    x = np.arange(ntask)
    width = 1  # the width of the bars

    fig, ax = plt.subplots(figsize=(9, 3))
    HUMANEVAL = r"\textsc{HumanEval}"
    HUMANEVAL_PLUS = r"\textsc{HumanEval\textsuperscript{+}}"
    rects1 = ax.bar(x, rate_old, color="coral", label=HUMANEVAL, alpha=0.5)
    rects2 = ax.bar(x, rate_new, color="darkorchid", label=HUMANEVAL_PLUS, alpha=0.8)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel("Average Pass Rate (\%)")
    ax.set_xlabel(f"Problems (Sorted by {HUMANEVAL} pass rate)")

    # turn off xticks
    ax.set_xticks([])
    ax.set_xticklabels([])
    # tight x ranges
    ax.set_xlim(-0.5, ntask - 0.5)

    # x grid
    ax.grid(linestyle="--", linewidth=1, alpha=0.8)

    # log scale
    ax.set_yscale("log")

    ax.legend()
    fig.tight_layout()

    plt.savefig("passrate.pdf", bbox_inches="tight")
    plt.savefig("passrate.png", bbox_inches="tight")

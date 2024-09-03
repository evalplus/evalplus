# for the same model, we first study which prompting strategy is better

import json
import os
import re
from collections import defaultdict
from statistics import mean

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from rich import print


def normalize_to_base_name(name: str) -> str:
    name = (
        name.replace("Chat", "")
        .replace("instruct", "")
        .replace("code-llama", "CodeLlama")
        .replace("deepseek-coder", "DeepSeek-Coder")
        .replace("gpt-4-turbo", "GPT-4-Turbo")
        .replace("starcoder", "StarCoder")
        .replace("--v0.1", "")
        .replace("-base", "")
        .replace("-preview", "")
        .strip("-")
    )
    # ${NUM}b -> ${NUM}B
    return re.sub(r"(\d+)b", r"\1B", name)


def load_dps_scores(path: str, norm: bool = False):
    with open(path) as f:
        results = json.load(f)

    task2score = {}
    for task_id, result in results.items():
        # new rpr
        new_key = "norm_scores" if norm else "scores"
        if result.get(new_key) is not None:
            task2score[task_id] = result[new_key]["avg"]
        # legacy rpr
        legacy_key = "dps_norm" if norm else "dps"
        if result.get(legacy_key) is not None:
            task2score[task_id] = mean(result[legacy_key])

    return task2score


# EvalPerf result file name format: {MODEL}_temp_{TEMP}_ep_{TYPE}_results.json
def parse_model_and_type(result_json: str):
    assert "_temp_0.2_" in result_json, f"Invalid result file name: {result_json}"
    model_id, rest = result_json.split("_temp_0.2_")
    type = rest.split("_")[1]
    model_id = normalize_to_base_name(model_id)
    # extra 6.7 in "DSCoder-6.7B" and "7B" in "DSCoder-7B"
    nb = re.search(r"(\d+(?:\.\d+)?)B", model_id)
    if nb:
        print(nb)
        nb = nb.group(1)
        model_id = model_id.replace(f"{nb}B", "").strip("-")
    else:
        nb = None
    return model_id, nb, type


def load_groups_from_directory(result_dir: str, norm: bool = False):
    groups = defaultdict(dict)  # model -> {type: dps(norm)}

    for result_json in os.listdir(result_dir):
        if not result_json.endswith(".json"):
            continue
        model_id, nb, type = parse_model_and_type(result_json)
        if not (type == "instruct" or (type == "base" and model_id == "StarCoder2")):
            continue

        if not nb:
            continue

        print(f"{type = :<16}\t{model_id = } {nb = }")
        model_id = f"{model_id} ({type})"
        groups[model_id][nb] = load_dps_scores(
            os.path.join(result_dir, result_json), norm
        )

    # sort the items by nb
    for model_id in groups:
        groups[model_id] = dict(
            sorted(groups[model_id].items(), key=lambda x: -float(x[0]))
        )

    # rename the keys to {nb}B
    groups = {
        model_id: {f"{nb}B": vv for nb, vv in v.items()}
        for model_id, v in groups.items()
    }

    return groups


def compute_score_matrix(group: dict):
    grp_keys = list(group.keys())
    score_matrix = []
    for i, type_x in enumerate(grp_keys):
        score_list = []
        for j, type_y in enumerate(grp_keys):
            if j <= i or type_y not in group or type_x not in group:
                score_list.append((0, 0))
                continue
            task2dps_x = group[type_x]
            task2dps_y = group[type_y]
            common_tasks = set(task2dps_x.keys()) & set(task2dps_y.keys())
            if not common_tasks:
                score_list.append(None)
                print(f"No common tasks between {type_x} and {type_y}")
                continue
            dps_x = mean([task2dps_x[task_id] for task_id in common_tasks])
            dps_y = mean([task2dps_y[task_id] for task_id in common_tasks])
            print(type_x, dps_x, " --- ", type_y, dps_y)
            score_list.append((dps_x, dps_y))
        score_matrix.append(score_list)
    return score_matrix


def main(result_dir: str, norm: bool = False, latex: bool = False):
    if latex:
        plt.rc("text", usetex=True)
        plt.rc("text.latex", preamble=r"\usepackage{xfrac}")
    assert os.path.isdir(result_dir), f"{result_dir} is not a directory."

    groups = load_groups_from_directory(result_dir, norm=norm)
    groups = {k: v for k, v in groups.items() if len(v) >= 2}
    # resort by key
    groups = dict(sorted(groups.items()))

    n_grp = len(groups)
    max_grp_per_row = 3
    n_row = (n_grp + max_grp_per_row - 1) // max_grp_per_row

    fig, axs = plt.subplots(
        n_row,
        max_grp_per_row,
        figsize=(2 * max_grp_per_row, 2 * n_row),
        constrained_layout=True,
    )

    for k, (model, group) in enumerate(groups.items()):
        grp_keys = list(group.keys())
        score_matrix = compute_score_matrix(group)
        score_matrix_diff = [
            [(score[0] - score[1]) for score in score_list]
            for score_list in score_matrix
        ]
        ax: plt.Axes = axs[k]
        cmap = LinearSegmentedColormap.from_list("rg", ["r", "w", "lime"], N=256)
        # ax.matshow(score_matrix_diff, cmap=cmap)
        cax = ax.matshow(score_matrix_diff, cmap=cmap)
        cax.set_clim(-25, 25)
        ax.set_xticks(range(len(grp_keys)))
        ax.set_yticks(range(len(grp_keys)))
        ax.set_xticklabels(grp_keys, rotation=30, ha="left", rotation_mode="anchor")
        ax.set_yticklabels(grp_keys)
        ax.tick_params(bottom=False)
        for i in range(len(grp_keys)):
            for j in range(len(grp_keys)):
                if j <= i:
                    continue
                x, y = score_matrix[i][j]  # i~x, j~y
                if x == 0 and y == 0:
                    continue
                gapx = 0.15
                gapy = 0.25
                ax.text(
                    j - gapx,
                    i + gapy,
                    f"{x:.1f}",
                    va="center",
                    ha="center",
                    color="green" if x > y else "red",
                )
                ax.text(
                    j + gapx,
                    i - gapy,
                    f"{y:.1f}",
                    va="center",
                    ha="center",
                    color="green" if x < y else "red",
                )
        xlabel = model
        if latex:
            xlabel = r"\textbf{" + xlabel + "}"
        ax.set_xlabel(xlabel)

    imname = "perf_param_impact"
    if norm:
        imname += "_norm"
    plt.savefig(f"{imname}.png", dpi=100, bbox_inches="tight")
    plt.savefig(f"{imname}.pdf", dpi=100, bbox_inches="tight")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)

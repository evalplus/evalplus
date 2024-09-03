import json
import os
from statistics import mean

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# EvalPerf result file name format: {MODEL}_temp_{TEMP}_ep-{TYPE}_results.json


# Draw a heatmap of pairwise comparison of models
# each pair of models is compared using the same set of passing tasks
def main(result_dir: str):
    assert os.path.isdir(result_dir), f"{result_dir} is not a directory."

    model2task2dps = {}
    model2task2dps_norm = {}

    model_list = []
    model_e2e_dps = []
    for result_json in os.listdir(result_dir):
        if not result_json.endswith(".json"):
            continue
        result_json_path = os.path.join(result_dir, result_json)
        assert "_temp_0.2_" in result_json, f"Invalid result file name: {result_json}"
        model_id = result_json.split("_temp_0.2_")[0]
        if model_id.endswith("-instruct") and not model_id.endswith(" perf-instruct"):
            model_id = model_id[: -len("-instruct")]
            model_id += " :: default"
        if "::" not in model_id:
            model_id += " :: default"
        print(f"Processing {model_id}")
        with open(result_json_path) as f:
            results = json.load(f)
        task2dps = {}
        task2dps_norm = {}

        for task_id, result in results.items():
            if "scores" in result and result["scores"] is not None:
                task2dps[task_id] = result["scores"]["max"]
                task2dps_norm[task_id] = result["norm_scores"]["max"]
            if "dps" in result and result["dps"] is not None:
                task2dps[task_id] = max(result["dps"])
                task2dps_norm[task_id] = max(result["dps_norm"])

        model2task2dps[model_id] = task2dps
        model2task2dps_norm[model_id] = task2dps_norm
        model_list.append(model_id)
        model_e2e_dps.append(mean(task2dps.values()))

    # sort model list by dps score
    model_list, model_e2e_dps = zip(
        *sorted(zip(model_list, model_e2e_dps), key=lambda x: x[1], reverse=True)
    )

    # model_list = model_list[:32]

    fig, ax = plt.subplots(figsize=(30, 25))

    score_matrix = []
    for i, model_x in enumerate(model_list):
        score_list = []
        task2dps_x = model2task2dps[model_x]
        for j, model_y in enumerate(model_list):
            if j <= i:
                score_list.append((0, 0))
                continue
            task2dps_y = model2task2dps[model_y]
            common_tasks = set(task2dps_x.keys()) & set(task2dps_y.keys())
            if len(common_tasks) == 0:
                score_list.append(None)
                print(
                    f"[Warning] no common passing set between {model_x} and {model_y}"
                )
                continue
            dps_x = mean([task2dps_x[task_id] for task_id in common_tasks])
            dps_y = mean([task2dps_y[task_id] for task_id in common_tasks])
            score_list.append((dps_x, dps_y))
            text = f"{round(dps_x)}"
            if dps_x - dps_y >= 1:
                text += f"\n+{dps_x - dps_y:.1f}"
            elif dps_x - dps_y <= -1:
                text += f"\n-{dps_y - dps_x:.1f}"
            ax.text(
                j,
                i,
                text,
                va="center",
                ha="center",
                color="green" if dps_x > dps_y else "red",
            )
        score_matrix.append(score_list)

    # print(score_matrix)

    score_matrix_diff = [
        [None if score is None else score[0] - score[1] for score in score_list]
        for score_list in score_matrix
    ]

    cmap = LinearSegmentedColormap.from_list("rg", ["r", "w", "lime"], N=256)
    cax = ax.matshow(score_matrix_diff, cmap=cmap)
    cax.set_clim(-15, 15)
    fig.colorbar(cax)
    ax.set_xticks(range(len(model_list)))
    ax.set_yticks(range(len(model_list)))
    ax.set_xticklabels(model_list, rotation=45, ha="left", rotation_mode="anchor")
    ax.set_yticklabels(model_list)
    # save fig
    plt.savefig("pairwise_heatmap.png", dpi=120, bbox_inches="tight")
    plt.savefig("pairwise_heatmap.pdf", bbox_inches="tight")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)

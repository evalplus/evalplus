import json
import os
import pickle

from rich.progress import track

from tools.tsr.utils import get_task_ids, to_path


def collect_sample_info(sample_dir: str, sample_eval_dir: str, dataset: str):
    if os.path.exists(sample_dir) and len(os.listdir(sample_dir)) > 0:
        # cache file exists
        return
    task_ids = get_task_ids(dataset)
    assert os.path.exists(sample_eval_dir), "sample evaluation files missing"
    os.makedirs(sample_dir, exist_ok=True)
    kill_info = {task_id: {} for task_id in task_ids}
    model_paths = os.listdir(sample_eval_dir)
    for model_path in track(model_paths, description="Collecting sets..."):
        if not model_path[-1].isdigit():
            continue
        eval_json_path = os.path.join(sample_eval_dir, model_path, "eval_results.json")
        if not os.path.exists(eval_json_path):
            continue
        with open(eval_json_path, "r") as f:
            res = json.load(f)["eval"]
            for task_id, v in res.items():
                if task_id not in task_ids:
                    continue
                for i_code, (status, res_list) in enumerate(v["plus"]):
                    if status == "success":
                        continue
                    for i_test, res in enumerate(res_list):
                        test_id = f"plus_{i_test}"
                        if res == False:
                            if "_" in task_id:
                                task_id = task_id.replace("_", "/")
                            kill_info[task_id].setdefault(test_id, []).append(
                                (model_path, i_code)
                            )
    for task_id in task_ids:
        path_task_id = to_path(task_id)
        with open(os.path.join(sample_dir, f"{path_task_id}.pkl"), "wb") as f:
            pickle.dump(kill_info[task_id], f)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--report_dir", required=True, type=str)
    parser.add_argument("--dataset", type=str, choices=["humaneval", "mbpp"])
    parser.add_argument("--sample_eval_dir", required=True, type=str)
    args = parser.parse_args()

    sample_dir = os.path.join(args.report_dir, "sample_cache")
    collect_sample_info(sample_dir, args.sample_eval_dir, args.dataset)

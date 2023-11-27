import os

from tools.tsr import tsr_base_dir
from tools.tsr.utils import execute_cmd

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, help="Model for testing")
    parser.add_argument("--dataset", type=str, choices=["humaneval", "mbpp"])
    parser.add_argument(
        "--report_dir",
        type=str,
        help="Path to JSON report and cache files",
        default=os.path.join(tsr_base_dir, "tsr_info"),
    )
    parser.add_argument(
        "--sample_eval_dir",
        type=str,
        required=True,
        help="Path to sample evaluation files",
    )
    args = parser.parse_args()

    os.makedirs(args.report_dir, exist_ok=True)
    execute_cmd(
        [
            "python3",
            os.path.join(tsr_base_dir, "mutation_init.py"),
            "--dataset",
            args.dataset,
            "--report_dir",
            args.report_dir,
        ]
    )
    execute_cmd(
        [
            "python3",
            os.path.join(tsr_base_dir, "coverage_init.py"),
            "--dataset",
            args.dataset,
            "--report_dir",
            args.report_dir,
        ]
    )
    execute_cmd(
        [
            "python3",
            os.path.join(tsr_base_dir, "sample_init.py"),
            "--report_dir",
            args.report_dir,
            "--sample_eval_dir",
            args.sample_eval_dir,
        ]
    )
    execute_cmd(
        [
            "python3",
            os.path.join(tsr_base_dir, "minimization.py"),
            "--dataset",
            args.dataset,
            "--model",
            args.model,
            "--report_dir",
            args.report_dir,
            "--sample_eval_dir",
            args.sample_eval_dir,
            "--mini_path",
            args.report_dir,
        ]
    )

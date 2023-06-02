import os

from evalplus.tsr.utils import execute_cmd

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, help="Model for testing")
    parser.add_argument(
        "--report_dir",
        type=str,
        help="Path to JSON report and cache files",
        default="./tsr_info",
    )
    parser.add_argument(
        "--sample_eval_dir",
        type=str,
        required=True,
        help="Path to sample evaluation files",
    )
    parser.add_argument(
        "--mini_path", type=str, default="./tsr_info", help="Path to Mini Dataset"
    )
    parser.add_argument("--mutation_only", action="store_true", default=False)
    args = parser.parse_args()

    os.makedirs("tsr_info", exist_ok=True)
    if args.mutation_only:
        execute_cmd(
            [
                "python3",
                "evalplus/tsr/mutation_init.py",
                "--report_dir",
                args.report_dir,
            ]
        )
    else:
        execute_cmd(
            [
                "python3",
                "evalplus/tsr/coverage_init.py",
                "--report_dir",
                args.report_dir,
            ]
        )
        execute_cmd(
            [
                "python3",
                "evalplus/tsr/sample_init.py",
                "--report_dir",
                args.report_dir,
                "--sample_eval_dir",
                args.sample_eval_dir,
            ]
        )
        execute_cmd(
            [
                "python3",
                "evalplus/tsr/minimization.py",
                "--model",
                args.model,
                "--report_dir",
                args.report_dir,
                "--sample_eval_dir",
                args.sample_eval_dir,
                "--mini_path",
                args.mini_path,
            ]
        )

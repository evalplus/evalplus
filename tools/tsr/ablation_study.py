import os
import subprocess

from rich.progress import track

models = [
    "codegen-2b",
    "codegen-6b",
    "codegen-16b",
    "codegen2-1b",
    "codegen2-3b",
    "codegen2-7b",
    "codegen2-16b",
    "vicuna-7b",
    "vicuna-13b",
    "stablelm-7b",
    "incoder-1b",
    "incoder-6b",
    "polycoder",
    "chatgpt",
    "santacoder",
    "starcoder",
    "gptneo-2b",
    "gpt-4",
    "gpt-j",
]


def execute_cmd(cmd_list):
    try:
        subprocess.run(cmd_list)
    except Exception as e:
        print(f"[Fail] {cmd_list}")
        print(str(e))


if __name__ == "__main__":
    for model in track(models):
        execute_cmd(
            [
                "python3",
                "tools/tsr/topk_tsr.py",
                "--model",
                model,
                "--stage",
                "s1",
                "--disable_coverage",
            ]
        )
        execute_cmd(
            [
                "python3",
                "tools/tsr/topk_tsr.py",
                "--model",
                model,
                "--stage",
                "s1",
                "--disable_mutation",
            ]
        )
        execute_cmd(
            [
                "python3",
                "tools/tsr/topk_tsr.py",
                "--model",
                model,
                "--stage",
                "s1",
                "--disable_sample",
            ]
        )
        execute_cmd(
            ["python3", "tools/tsr/topk_tsr.py", "--model", model, "--stage", "s1"]
        )

        execute_cmd(
            [
                "python3",
                "tools/tsr/topk_tsr.py",
                "--model",
                model,
                "--stage",
                "s2",
                "--disable_coverage",
            ]
        )
        execute_cmd(
            [
                "python3",
                "tools/tsr/topk_tsr.py",
                "--model",
                model,
                "--stage",
                "s2",
                "--disable_mutation",
            ]
        )
        execute_cmd(
            [
                "python3",
                "tools/tsr/topk_tsr.py",
                "--model",
                model,
                "--stage",
                "s2",
                "--disable_sample",
            ]
        )
        execute_cmd(
            ["python3", "tools/tsr/topk_tsr.py", "--model", model, "--stage", "s2"]
        )

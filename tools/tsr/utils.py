import os
import subprocess
from typing import List

from evalplus.data import get_human_eval_plus, get_mbpp_plus

HUMANEVAL_COUNT = 164
MBPP_COUNT = 399
humaneval_problems = get_human_eval_plus()
mbpp_problems = get_mbpp_plus()

humaneval_task_ids = [f"HumanEval/{i}" for i in range(HUMANEVAL_COUNT)]


def get_problems(dataset: str):
    return globals()[f"{dataset}_problems"]


def get_task_ids(dataset: str) -> List[str]:
    problems = globals()[f"{dataset}_problems"]
    return list(problems.keys())


def to_path(task_id: str) -> str:
    return task_id.replace("/", "_")


def clean(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)


def execute_cmd(cmd: list):
    os.system(" ".join(cmd))


def get_cmd_output(cmd_list: list) -> str:
    return subprocess.run(cmd_list, stdout=subprocess.PIPE, check=True).stdout.decode()

import os
import subprocess

from evalplus.data import get_human_eval_plus

HUMANEVAL_COUNT = 164
problems = get_human_eval_plus()

task_ids = [f"HumanEval/{i}" for i in range(HUMANEVAL_COUNT)]


def to_path(task_id: str) -> str:
    assert task_id in task_ids, f"invalid task_id = {task_id}"
    return task_id.replace("/", "_")


def clean(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)


def execute_cmd(cmd: list):
    os.system(" ".join(cmd))


def get_cmd_output(cmd_list: list) -> str:
    return subprocess.run(cmd_list, stdout=subprocess.PIPE, check=True).stdout.decode()

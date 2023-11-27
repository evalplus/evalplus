import os
import pickle
import sys
from importlib import import_module
from io import StringIO
from typing import Any, Dict, List

import coverage
from rich.progress import track

from evalplus.eval.utils import swallow_io
from tools.tsr.utils import get_problems, get_task_ids, to_path


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


def parse_lcov(outputs: List[str]):
    switch, extracted_outputs = False, []
    for line in outputs:
        if switch == False and "tmp_src" in line:
            switch = True
        if switch == True and "end_of_record" in line:
            switch = False
        if switch:
            extracted_outputs.append(line)

    branch, branch_covered = [], []
    for line in extracted_outputs:
        if line.startswith("BRDA"):
            # BRDA format: BR:<lineno>,<blockno>,<branchno>,<taken>
            lineno, blockno, branchno, taken = line[5:].split(",")
            branch_sig = f"BR:{lineno},{blockno},{branchno}"
            branch.append(branch_sig)
            if taken not in ["0", "-"]:
                branch_covered.append(branch_sig)
    per = 1.0 if len(branch) == 0 else len(branch_covered) / len(branch)
    return per, branch, branch_covered


def test_code_coverage(
    identifier: str, code: str, inputs: List[List[Any]], entry_point: str
):
    module_name = f"tmp_src_{identifier}"
    with open(f"{module_name}.py", "w") as f:
        f.write(code)

    mod = import_module(module_name)
    func = getattr(mod, entry_point, None)
    assert func != None, f"entry_point = {entry_point} not exist, code: {code}"

    cov = coverage.Coverage(branch=True)
    cov.start()
    with swallow_io():
        for input_list in inputs:
            func(*input_list)
    cov.stop()
    with Capturing() as outputs:
        cov.lcov_report(outfile="-")

    ret = parse_lcov(outputs)

    os.remove(f"{module_name}.py")
    return ret


def collect_coverage_info(coverage_dir: str, dataset: str) -> Dict[str, Dict[str, Any]]:
    os.makedirs(coverage_dir, exist_ok=True)
    problems = get_problems(dataset)
    task_ids = get_task_ids(dataset)
    coverage_info = {task_id: {} for task_id in task_ids}
    for task_id in track(task_ids, description="Testing gt coverage..."):
        coverage_cache_path = os.path.join(coverage_dir, f"{to_path(task_id)}.pkl")
        if os.path.isfile(coverage_cache_path):
            with open(coverage_cache_path, "rb") as f:
                coverage_info[task_id] = pickle.load(f)
            continue
        groundtruth_code = (
            problems[task_id]["prompt"] + problems[task_id]["canonical_solution"]
        )
        plus_tests = problems[task_id]["plus_input"]
        entry_point = problems[task_id]["entry_point"]
        for i, plus_test in enumerate(plus_tests):
            per, branch, branch_covered = test_code_coverage(
                to_path(task_id), groundtruth_code, [plus_test], entry_point
            )
            test_id = f"plus_{i}"
            coverage_info[task_id].setdefault(test_id, []).extend(
                [(br, "gt") for br in branch_covered]
            )
        with open(coverage_cache_path, "wb") as f:
            pickle.dump(coverage_info[task_id], f)

    return coverage_info


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, choices=["humaneval", "mbpp"])
    parser.add_argument("--report_dir", required=True, type=str)
    args = parser.parse_args()

    coverage_dir = os.path.join(args.report_dir, "coverage_cache")
    collect_coverage_info(coverage_dir, args.dataset)

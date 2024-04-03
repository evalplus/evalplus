import argparse
import importlib
import inspect
import multiprocessing
import os
import sys
from io import StringIO
from typing import Any, Callable, List, Union

import coverage

from evalplus.data import get_human_eval_plus
from evalplus.data.utils import to_raw
from evalplus.eval.utils import reliability_guard, swallow_io, time_limit


def construct_inputs_sig(inputs: list) -> str:
    str_builder = ""
    for x in inputs:
        if type(x) == str:
            str_builder += f"'{to_raw(x)}',"
        else:
            str_builder += f"{x},"
    return str_builder[:-1]


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


def parse_lcov(outputs: List[str], func: Callable, mode: str = "branch"):
    switch, extracted_outputs = False, []
    for line in outputs:
        if switch == False and "tmp_src" in line:
            switch = True
        if switch == True and "end_of_record" in line:
            switch = False
        if switch:
            extracted_outputs.append(line)

    src, start_lineno = inspect.getsourcelines(func)
    end_lineno = start_lineno + len(src) - 1

    if mode == "branch":
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
    else:
        not_covered_lines = []
        for line in extracted_outputs:
            if line.startswith("DA"):
                # DA format: DA:<lineno>,<exec_count>[,...]
                lineno, exec_count = line[3:].split(",")[:2]
                if start_lineno <= int(lineno) <= end_lineno:
                    if exec_count == "0":
                        not_covered_lines.append(int(lineno))
        for lineno in not_covered_lines:
            line = src[lineno - start_lineno]
            if line.strip() != "" and "def" not in line:
                src[lineno - start_lineno] = line[:-1] + "  # Not executed\n"
        return "".join(src)


def test_code_coverage(
    code: str, inputs: List[List[Any]], entry_point: str, mode="branch"
):
    def safety_test(code: str, inputs: List[List[Any]], entry_point: str):
        for input_list in inputs:
            code += f"{entry_point}({construct_inputs_sig(input_list)})\n"
        reliability_guard()
        try:
            with swallow_io():
                with time_limit(1):
                    exec(code, {})
        except:
            sys.exit(1)

    p = multiprocessing.Process(target=safety_test, args=(code, inputs, entry_point))
    p.start()
    p.join()
    safe = p.exitcode == 0
    if p.is_alive():
        p.terminate()
        p.kill()
    if not safe:
        print("Potentially dangerous code, refuse coverage test.")
        return None

    with open("tmp_src.py", "w") as f:
        f.write(code)
    import tmp_src

    importlib.reload(tmp_src)
    func = getattr(tmp_src, f"{entry_point}", None)
    assert func != None, f"{entry_point = } not exist"

    cov = coverage.Coverage(branch=True)
    cov.start()
    with swallow_io():
        for input_list in inputs:
            func(*input_list)
    cov.stop()
    with Capturing() as outputs:
        cov.lcov_report(outfile="-")

    ret = parse_lcov(outputs, func, mode)

    os.remove("tmp_src.py")
    return ret


def test_solution_coverage(
    dataset: str = "HumanEvalPlus",
    task_id: str = "HumanEval/0",
    impl: str = "canonical",
    inputs: Union[str, List[List[Any]]] = "base_input",
    mode: str = "branch",
):
    """
    Parameters:
    * dataset: {None, "HumanEval", "HumanEvalPlus"}
    * task_id: ralated to dataset
    * impl: {"canonical", source code}
    * inputs: {"base_inputs", list}
    * mode: {"branch"}, will support "line" for coverage-guided LLM test generation
    """
    if "HumanEval" in dataset:
        problems, problem = get_human_eval_plus(), None
        for p in problems:
            if p["task_id"] == task_id:
                problem = p
        assert problem != None, f"invalid {task_id = }"
        entry_point = problem["entry_point"]
        code = problem["prompt"] + (
            impl if impl != "canonical" else problem["canonical_solution"]
        )
        if inputs == "base_input":
            inputs = problem["base_input"]
    else:
        raise NotImplementedError

    return test_code_coverage(code, inputs, entry_point, mode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", type=str, default="branch", choices=["line", "branch"]
    )
    args = parser.parse_args()

    if args.mode == "branch":
        for i in range(0, 164):
            task_id = f"HumanEval/{i}"
            branch, branch_covered = test_solution_coverage(
                dataset="HumanEval", task_id=task_id, mode="branch"
            )
            per = 1.0 if len(branch) == 0 else len(branch_covered) / len(branch)
            if per != 1.0:
                print(i, per, len(branch_covered), len(branch))
    else:
        for i in range(0, 164):
            task_id = f"HumanEval/{i}"
            annotated_code = test_solution_coverage(
                dataset="HumanEval", task_id=task_id, mode="line"
            )
            if "Not executed" in annotated_code:
                print(f"{task_id = }")
                print(annotated_code)

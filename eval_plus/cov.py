import importlib
import inspect
import multiprocessing
import os
import sys
from io import StringIO
from typing import Any, Callable, List

import coverage

from eval_plus.evaluation.evaluate import construct_inputs_sig
from eval_plus.evaluation.evaluate_helpers import (
    reliability_guard,
    swallow_io,
    time_limit,
)


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
                if start_lineno <= int(lineno) <= end_lineno:
                    branch_sig = f"BR:{lineno},{blockno},{branchno}"
                    branch.append(branch_sig)
                    if taken not in ["0", "-"]:
                        branch_covered.append(branch_sig)
        return branch, branch_covered
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


def cov(code: str, inputs: List[List[Any]], entry_point: str, mode="branch"):
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

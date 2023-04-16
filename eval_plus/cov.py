import sys
import coverage, inspect

from typing import Callable
from io import StringIO


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


def test_coverage(func: Callable, inputs: list):
    src, start_lineno = inspect.getsourcelines(func)
    end_lineno = start_lineno + len(src) - 1

    try:
        cov = coverage.Coverage(branch=True)
        cov.start()
        try:
            func(*inputs)
        except: pass
        cov.stop()
        with Capturing() as outputs:
            cov.lcov_report(outfile="-")
    except coverage.CoverageException:
        return [], []

    branch, branch_covered = [], []
    for output in outputs:
        if output.startswith("BRDA"):
            # branch coverage format:
            #   BRDA:<line number>,<block number>,<branch number>,<taken>
            lineno, blockno, branchno, taken = output[5:].split(",")
            if start_lineno <= int(lineno) <= end_lineno:
                branch_sig = f"BR:{lineno},{blockno},{branchno}"
                branch.append(branch_sig)
                if taken not in ["0", "-"]:
                    branch_covered.append(branch_sig)

    return branch, branch_covered
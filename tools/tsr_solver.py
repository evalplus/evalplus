from typing import List, Optional

import pulp


class TSRSolver:
    def __init__(self, num_tests: int):
        self.num_tests = num_tests
        self.t = []
        for i in range(num_tests):
            self.t.append(pulp.LpVariable(f"t{i}", cat="Binary"))

    def solve(self, requirements: List[List[int]]) -> Optional[List[int]]:
        s = pulp.LpProblem()
        s += sum(self.t)
        for r in requirements:
            assert (
                len(r) == self.num_tests + 1
            ), "Requirement format not correct!\nExpected format: [c1, c2, ...., cn, threshold]"
            s += sum(r[i] * self.t[i] for i in range(self.num_tests)) >= r[-1]
        s.solve(pulp.PULP_CBC_CMD(msg=0))
        res = [0] * self.num_tests
        for v in s.variables():
            res[int(v.name[1:])] = int(v.varValue)
        return res


if __name__ == "__main__":
    import random

    num = 1000
    s = TSRSolver(num)
    r = []
    for i in range(10):
        r.append([random.randint(2, 5) for i in range(num - 1)] + [1000])
    print(s.solve(r))

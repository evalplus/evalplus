import argparse
from typing import Any, List, Union

from appdirs import user_cache_dir

from eval_plus.cov import cov
from eval_plus.utils import get_human_eval_plus


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

    return cov(code, inputs, entry_point, mode)


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

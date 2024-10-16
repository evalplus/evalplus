import ast
import json
import multiprocessing
import os
import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, List

import astor
import black
from tqdm import tqdm

from evalplus.data import (
    get_human_eval_plus,
    get_human_eval_plus_hash,
    get_mbpp_plus,
    get_mbpp_plus_hash,
)
from evalplus.eval import PASS
from evalplus.evalperf import correctness_check
from evalplus.evaluate import get_groundtruth


def find_calls(source, functors, skip_main_fn=True):
    class FunctorVisitor(ast.NodeVisitor):
        def __init__(self, target_functors):
            super().__init__()
            self.target_functors = target_functors
            self._temp_found_functors = set()
            self.results = []

        def visit_FunctionDef(self, node):
            self.current_function = node.name
            self._temp_found_functors = set()
            self.generic_visit(node)  # Continue traversing child nodes
            if self._temp_found_functors:
                self.results.append((self.current_function, self._temp_found_functors))

        # visit func def
        def visit_FunctionDef(self, node: ast.FunctionDef):
            if skip_main_fn and node.name == "main":
                return
            # visit child nodes
            self.generic_visit(node)

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name) and node.func.id in self.target_functors:
                self._temp_found_functors.add(node.func.id)
            self.generic_visit(node)

    tree = ast.parse(source)
    visitor = FunctorVisitor(target_functors=functors)
    visitor.visit(tree)
    return {caller: callee for caller, callee in visitor.results}


def void_calls(source, functors, skip_main_fn=True):
    changed = False

    class FunctorTransformer(ast.NodeTransformer):
        def __init__(self, target_functors):
            super().__init__()
            self.target_functors = target_functors

        # visit func def
        def visit_FunctionDef(self, node: ast.FunctionDef):
            if skip_main_fn and node.name == "main":
                return node
            # visit child nodes
            return self.generic_visit(node)

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name) and node.func.id in self.target_functors:
                nonlocal changed
                changed = True
                return ast.Expr(value=ast.Constant(value=None))
            return node

    tree = ast.parse(source)
    code = astor.to_source(FunctorTransformer(functors).visit(tree))
    fmt_code = black.format_str(code, mode=black.FileMode())
    return (fmt_code, changed)


def has_print_in_non_main_functions(source) -> bool:
    for caller, _ in find_calls(source, ["print"]).items():
        if caller != "main":
            return True
    return False


def gather_solutions(sample_path: str, task_id: str) -> List[str]:
    """Gather all solutions from the folders"""
    solutions = []
    for model in os.listdir(sample_path):
        model_path = os.path.join(sample_path, model)
        if not os.path.isdir(model_path):
            continue
        task_path = os.path.join(model_path, task_id)
        if os.path.isdir(task_path):
            for file in os.listdir(task_path):
                if file.endswith(".py"):
                    with open(os.path.join(task_path, file), "r") as f:
                        solutions.append(f.read())
    return solutions


def deduplicate(solutions: List[str]) -> List[str]:
    """Deduplicate solutions"""
    asts = set()
    deduplicated = []
    for solution in solutions:
        solution = re.sub(r"#[^\n]*", "", solution)
        solution = re.sub(r'"""[^"]*"""', "", solution)
        solution = re.sub(r"'''[^']*'''", "", solution)
        try:
            ast_string = ast.dump(ast.parse(solution))
        except SyntaxError:
            continue
        except MemoryError:
            continue
        if ast_string not in asts:
            asts.add(ast_string)
            deduplicated.append(solution)
    return list(deduplicated)


def test_solutions(
    dataset: str, solutions: List[str], task: Dict, expected_output: List
) -> List[str]:
    """Test solutions, return functionally correct solutions"""
    n_workers = max(1, multiprocessing.cpu_count() // 2)
    correct_solution_ids = []

    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = [
            executor.submit(
                correctness_check, index, solution, dataset, task, expected_output
            )
            for index, solution in enumerate(solutions)
        ]
        for future in as_completed(futures):
            index, result, _ = future.result()
            if result[0] == PASS:
                correct_solution_ids.append(index)

    return [solutions[i] for i in correct_solution_ids]


def script(sample_dir: str, dataset: str = "humaneval", debug_task: str = None):
    assert dataset in ["humaneval", "mbpp"]
    if dataset == "humaneval":
        problems = get_human_eval_plus(noextreme=True)
        dataset_hash = get_human_eval_plus_hash(noextreme=True)
        expected_output = get_groundtruth(problems, dataset_hash, [])
    elif dataset == "mbpp":
        from evalplus.eval._special_oracle import MBPP_OUTPUT_NOT_NONE_TASKS

        problems = get_mbpp_plus(noextreme=True)
        dataset_hash = get_mbpp_plus_hash(noextreme=True)
        expected_output = get_groundtruth(
            problems,
            dataset_hash,
            MBPP_OUTPUT_NOT_NONE_TASKS,
        )

    previous_solutions = None

    for task_id, task in tqdm(problems.items()):
        if debug_task and task_id != debug_task:
            continue
        solutions = gather_solutions(sample_dir, task_id.replace("/", "_"))
        solutions = deduplicate(solutions)
        correct_solutions = test_solutions(
            dataset, solutions, task, expected_output[task_id]
        )

        # clean solutions to remove print statements and format it
        correct_solutions = [
            void_calls(solution, ["print"])[0] for solution in correct_solutions
        ]

        # Assuming that the previous solutions are correct
        if previous_solutions and task_id in previous_solutions:
            correct_solutions = deduplicate(
                correct_solutions + previous_solutions[task_id]
            )
        with open("solutions.jsonl", "a+") as f:
            f.write(
                json.dumps({"task_id": task_id, "solution": correct_solutions}) + "\n"
            )


def main():
    from fire import Fire

    Fire(script)


if __name__ == "__main__":
    main()

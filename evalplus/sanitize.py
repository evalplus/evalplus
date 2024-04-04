"""Post-processing LLM-generated Python code implemented using tree-sitter."""

import os
import pathlib
from typing import Dict, Generator, List, Optional, Set, Tuple

from tqdm import tqdm
from tree_sitter import Node
from tree_sitter_languages import get_parser

from evalplus.data import (
    get_human_eval_plus,
    get_mbpp_plus,
    load_solutions,
    write_directory,
    write_jsonl,
)
from evalplus.syncheck import syntax_check

CLASS_TYPE = "class_definition"
FUNCTION_TYPE = "function_definition"
IMPORT_TYPE = ["import_statement", "import_from_statement"]
IDENTIFIER_TYPE = "identifier"
ATTRIBUTE_TYPE = "attribute"
RETURN_TYPE = "return_statement"
EXPRESSION_TYPE = "expression_statement"
ASSIGNMENT_TYPE = "assignment"


def code_extract(text: str) -> str:
    lines = text.split("\n")
    longest_line_pair = (0, 0)
    longest_so_far = 0

    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            current_lines = "\n".join(lines[i : j + 1])
            if syntax_check(current_lines):
                current_length = sum(1 for line in lines[i : j + 1] if line.strip())
                if current_length > longest_so_far:
                    longest_so_far = current_length
                    longest_line_pair = (i, j)

    return "\n".join(lines[longest_line_pair[0] : longest_line_pair[1] + 1])


def get_callee_name(
    node: Node, class_names: Set[str], function_names: Set[str]
) -> Optional[str]:
    for child in node.children:
        if child.type == ATTRIBUTE_TYPE:
            name = child.children[0].text.decode("utf8")
            if name in class_names:
                return name
        elif child.type == IDENTIFIER_TYPE:
            name = child.text.decode("utf8")
            if name in function_names or name in class_names:
                return name


def get_call_graph(
    nodes: List[Tuple[str, Node]], class_names: Set[str], function_names: Set[str]
) -> Dict[str, str]:
    call_graph = {}
    for name, node in nodes:
        function_calls = []
        traverse_nodes = traverse_tree(node)
        for node in traverse_nodes:
            if node.type == "call":
                callee_name = get_callee_name(node, class_names, function_names)
                if callee_name:
                    function_calls.append(callee_name)
        call_graph[name] = function_calls
    return call_graph


def get_function_dependency(entrypoint: str, call_graph: Dict[str, str]) -> Set[str]:
    queue = [entrypoint]
    visited = set([entrypoint])
    while len(queue) != 0:
        current = queue.pop(0)
        for neighbour in call_graph[current]:
            if not (neighbour in visited):
                visited.add(neighbour)
                queue.append(neighbour)
    return visited


def get_definition_name(node: Node) -> str:
    for child in node.children:
        if child.type == IDENTIFIER_TYPE:
            return child.text.decode("utf8")


def traverse_tree(node: Node) -> Generator[Node, None, None]:
    cursor = node.walk()
    depth = 0

    visited_children = False
    while True:
        if not visited_children:
            yield cursor.node
            if not cursor.goto_first_child():
                depth += 1
                visited_children = True
        elif cursor.goto_next_sibling():
            visited_children = False
        elif not cursor.goto_parent() or depth == 0:
            break
        else:
            depth -= 1


def has_return_statement(node: Node) -> bool:
    traverse_nodes = traverse_tree(node)
    for node in traverse_nodes:
        if node.type == RETURN_TYPE:
            return True
    return False


def sanitize(code: str, entrypoint: Optional[str] = None) -> str:
    code = code_extract(code)
    parser = get_parser("python")
    tree = parser.parse(bytes(code, "utf8"))
    class_names = set()
    function_names = set()
    variable_names = set()

    root_node = tree.root_node
    import_nodes = []
    definition_nodes = []

    for child in root_node.children:
        if child.type in IMPORT_TYPE:
            import_nodes.append(child)
        elif child.type == CLASS_TYPE:
            name = get_definition_name(child)
            if not (
                name in class_names or name in variable_names or name in function_names
            ):
                definition_nodes.append((name, child))
                class_names.add(name)
        elif child.type == FUNCTION_TYPE:
            name = get_definition_name(child)
            if not (
                name in function_names or name in variable_names or name in class_names
            ) and has_return_statement(child):
                definition_nodes.append((name, child))
                function_names.add(get_definition_name(child))
        elif (
            child.type == EXPRESSION_TYPE and child.children[0].type == ASSIGNMENT_TYPE
        ):
            subchild = child.children[0]
            name = get_definition_name(subchild)
            if not (
                name in variable_names or name in function_names or name in class_names
            ):
                definition_nodes.append((name, subchild))
                variable_names.add(name)

    if entrypoint:
        call_graph = get_call_graph(definition_nodes, class_names, function_names)
        reacheable = get_function_dependency(entrypoint, call_graph)

    sanitized_output = ""

    for node in import_nodes:
        sanitized_output += code[node.start_byte : node.end_byte] + "\n"

    for pair in definition_nodes:
        name, node = pair
        if not (name in variable_names) and entrypoint and not (name in reacheable):
            continue
        sanitized_output += code[node.start_byte : node.end_byte] + "\n"
    return sanitized_output[:-1]


def main(samples: str, inplace: bool = False, debug_task: str = None):
    # task_id -> entry_point
    entry_point = {}
    # merge two datasets
    dataset = {**get_human_eval_plus(), **get_mbpp_plus()}

    for task_id, problem in dataset.items():
        entry_point[task_id] = problem["entry_point"]

    # make a new folder with "-sanitized" suffix
    is_folder = os.path.isdir(samples)
    target_path = pathlib.Path(samples)
    if not inplace:
        if is_folder:
            new_name = target_path.name + "-sanitized"
        else:
            new_name = target_path.name.replace(".jsonl", "-sanitized.jsonl")
        target_path = target_path.parent / new_name
    target_path = str(target_path)

    nsan = 0
    ntotal = 0

    new_solutions = []

    for solution in tqdm(load_solutions(samples)):
        task_id = solution["task_id"]
        function_name = entry_point[task_id] if task_id in entry_point else None
        dbg_identifier = solution["_identifier"]
        if debug_task is not None and task_id != debug_task:
            continue

        ntotal += 1
        if "solution" in solution:
            old_code = solution["solution"]
        else:
            assert "completion" in solution
            old_code = dataset[task_id]["prompt"] + "\n" + solution["completion"]

        new_code = sanitize(code=old_code, entrypoint=function_name)

        # if changed, print the message
        if new_code != old_code:
            msg = "Sanitized: " + dbg_identifier
            if is_folder:
                msg += " -> " + dbg_identifier.replace(samples, target_path)
            print(msg)
            nsan += 1

        new_solutions.append({"task_id": task_id, "solution": new_code})

    if is_folder:
        write_directory(target_path, new_solutions)
    else:
        write_jsonl(target_path, new_solutions)

    if nsan > 0:
        print(f"Sanitized {nsan} out of {ntotal} files.")
    else:
        print(f"All files seems valid -- no files are sanitized.")
    print(f"Check the sanitized files at {target_path}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)

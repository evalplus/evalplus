# EvalPlus

## HOWTO

```python
from eval_plus.utils import get_human_eval_plus

fe = get_human_eval_plus() # -> a list of tasks (each is a dict)
# "task_id" is the identifier string for the task.
# "prompt" is the function signature with docstring.
# "contract" is the assertions for the function's input (empty if no constraints).
# "canonical_solution" is the ground-truth implementation.
# "base_input" is the test inputs.
# "atol": absolute tolerance for diff-testing
```

> **Note**:
> + To build a HumanEval prompt: use `prompt`
> + To build a prompt with contracts: use `prompt` + `contract`
> + The program should work without `contract` (Run `python tools/check_ground_truth.py` to check)

## Development

Before you start:

```bash
pip install -r requirements.txt
pre-commit install
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### Name Convention

- `eval_plus` is the package name.
- `${DATASET}_plus` is the name of dataset applied with `eval_plus`.

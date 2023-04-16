# EvalPlus

## HOWTO

```python
from eval_plus.utils import get_human_eval_plus

fe = get_human_eval_plus() # -> a list of tasks (each is a dict)
# "task_id" is the identifier string for the task.
# "prompt" is the function signature with docstring.
# "contract" is the assertions for the function's input (empty if no constraints).
# "isignature" is the function's input signature.
# "docstring" is the docstring.
# "reference" is the ground-truth implementation for diff-testing.
# "base_input" is the test inputs.

# To build a HumanEval prompt: use "prompt"
# To build a prompt with contracts: use "prompt" + "contract"
```

> **Warning**
> The "reference" field is incomplete for some tasks (i.e., `    pass`). Check before use!

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

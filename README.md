# FuzzEval

## HOWTO

```python
from fuzz_eval.utils import get_fuzz_eval

fe = get_fuzz_eval() # -> a list of tasks (each is a dict)
# "task_id" is the identifier string for the task.
# "prompt" is the function signature with docstring.
# "isignature" is the function's input signature.
# "docstring" is the docstring.
# "reference" is the ground-truth implementation for diff-testing.
# "base_input" is the test inputs.
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

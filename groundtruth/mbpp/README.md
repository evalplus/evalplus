## Add contract

- Add some assertions for the arguments (types, values, etc.)
- Use `"invalid inputs"` as the assertion message.
- Mark the line with `# $_CONTRACT_$` in the end of the line (don't break the line!)

```python
def square_int(x: int) -> int:
    assert isinstance(x, int), "invalid inputs" # $_CONTRACT_$
    assert x >= 0, "invalid inputs" # $_CONTRACT_$
    return x * x
```

## Check implementation

The implementation can be buggy so fix it if you find any bugs.

### Quirky implemetations and tests
some implementations/tests are quirky and maybe buggy.
- [100](100.py#L9): unused variable
- [101](101.py#L8-L12): a weird and useless sort
- [115](115.py#L12-L13): the input should be list of dict, but the test case input is dict/list of set

## Commit message

```shell
git add groundtruth/mbpp/
git commit -m 'contract[mbpp]: 001'
git push origin mbpp
```

## Test

```shell
python tools/mbpp/check_ground_truth.py
```
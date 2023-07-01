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
- [100](100.py#L9): unused variable ([fixed](https://github.com/evalplus/evalplus/commit/9ff4fd361dc4a340d30d37f5d0649b4b43d33462))
- [101](101.py#L8-L12): wrong implementation; sorting is unnecessary ([fixed](https://github.com/evalplus/evalplus/commit/67c744d4b124090000d80217a7f7a1dee0d82b55))
- [115](115.py#L12-L13): wrong test case and implementation ([fixed](https://github.com/evalplus/evalplus/commit/4fa8a570814d4f232b57a8c9d6951b783a9c1c81))
- [127](127.py): unnecessarily complicated ([fixed](https://github.com/evalplus/evalplus/commit/04d99e88e1117d2f327865a15ad76a2a5e3f0d86))
- [143](143.py): wrong implementation ([fixed](https://github.com/evalplus/evalplus/commit/0a85efe6709d8f288d42b8ae913a9ff847ee6a88))

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
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

Some implementations/tests are quirky and maybe buggy.

- [020](020.py): wrong implementation (negative/float)
- [100](100.py): unused variable ([fixed](https://github.com/evalplus/evalplus/commit/9ff4fd361dc4a340d30d37f5d0649b4b43d33462))
- [101](101.py): wrong implementation; sorting is unnecessary ([fixed](https://github.com/evalplus/evalplus/commit/67c744d4b124090000d80217a7f7a1dee0d82b55))
- [115](115.py): wrong test case and implementation ([fixed](https://github.com/evalplus/evalplus/commit/56013c437ce689cfca6c7e98e4185577edc6b450))
- [127](127.py): unnecessarily complicated ([fixed](https://github.com/evalplus/evalplus/commit/410a932afedb2a0568aa5ef68b2df83aa35e7c1e))
- [143](143.py): wrong test case and implementation ([fixed](https://github.com/evalplus/evalplus/commit/9c189569ea363ed4b7fc960c0dc617c85fea143f))
- [307](307.py): broken problem description and implementation (this problem is broken which is also found by [ohters](https://www.youtube.com/watch?v=AQTgq-pDjy8))
- [406](406.py): wrong implementation;
- [429](429.py): wrong implementation: cannot meet the problem
- [444](444.py): wrong implementation: trim each tuple by k, not 2*k; str() is unnecessary
- [455](455.py): wrong implementation(?): No month number check
- [582](582.py): wrong test case and unnecessarily complicated implementation ([fixed](https://github.com/evalplus/evalplus/commit/0b34c263f36fde2997b87951f953585fb01c5267))
- [612](612.py): testcase does not align with the problem description 
- [723](723.py): wrong testcase: two list are not same length ([fixed](https://github.com/evalplus/evalplus/commit/90330578fb5913a13d224a7df92dc2d2dc70c77a))
- [733](733.py): wrong testcase: the array is not sorted([fixed](https://github.com/evalplus/evalplus/commit/47336f5404a282208e4673a5ffb7548b8dd65c04))
- [793](793.py): wrong testcase: the array is not sorted([fixed](https://github.com/evalplus/evalplus/commit/f0470f6ee59e7ac918ebc2c93177635f1a3451b6))

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

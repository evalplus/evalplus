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

### Ambiguous problem description
- [083](083.py): problem description is not align with the test cases

### Quirky implemetations and tests

Some implementations/tests are quirky and maybe buggy.

issues shown in italics are less important, such as redundant argument, duplicate problem, etc.

- [020](020.py): wrong implementation not considering float/negative ([fixed](https://github.com/evalplus/evalplus/commit/8a06cc1f7ba0c37672e34aa75c01ff0f031d48a4))
- [083](083.py): wrong implementation (fixed)
- [084](084.py): performance issue (fixed with non-recursive implementation)
- [089](089.py): broken problem description (fixed by `number` => `integer`)
- [100](100.py): unused variable ([fixed](https://github.com/evalplus/evalplus/commit/9ff4fd361dc4a340d30d37f5d0649b4b43d33462))
- [101](101.py): wrong implementation; sorting is unnecessary ([fixed](https://github.com/evalplus/evalplus/commit/67c744d4b124090000d80217a7f7a1dee0d82b55))
- [115](115.py): wrong test case and implementation ([fixed](https://github.com/evalplus/evalplus/commit/56013c437ce689cfca6c7e98e4185577edc6b450))
- [127](127.py): unnecessarily complicated ([fixed](https://github.com/evalplus/evalplus/commit/410a932afedb2a0568aa5ef68b2df83aa35e7c1e))
- [143](143.py): wrong test case and implementation ([fixed](https://github.com/evalplus/evalplus/commit/9c189569ea363ed4b7fc960c0dc617c85fea143f))
- [307](307.py): broken problem description and implementation (this problem is broken which is also found by [ohters](https://www.youtube.com/watch?v=AQTgq-pDjy8))
- [406](406.py): wrong and unnecessarily complex implementation ([fixed](https://github.com/evalplus/evalplus/commit/9d350b6bcb291512379fe07ccdf7c58ed5d72ad4))
- [444](444.py): vague description of "trim" and unnecessarily complex output format ([fixed](https://github.com/evalplus/evalplus/commit/9d350b6bcb291512379fe07ccdf7c58ed5d72ad4))
- [582](582.py): wrong test case and unnecessarily complicated implementation ([fixed](https://github.com/evalplus/evalplus/commit/0b34c263f36fde2997b87951f953585fb01c5267))
- [612](612.py): testcase does not align with the problem description 
- [723](723.py): wrong testcase: two list are not same length ([fixed](https://github.com/evalplus/evalplus/commit/90330578fb5913a13d224a7df92dc2d2dc70c77a))
- [733](733.py): wrong testcase: the array is not sorted([fixed](https://github.com/evalplus/evalplus/commit/47336f5404a282208e4673a5ffb7548b8dd65c04))
- [793](793.py): wrong testcase: the array is not sorted([fixed](https://github.com/evalplus/evalplus/commit/f0470f6ee59e7ac918ebc2c93177635f1a3451b6))
- [100](100.py): performance issue([fixed](https://github.com/evalplus/evalplus/commit/528d85a499419200dea5f07f7255993410ac30a0))
- [117](117.py): bad logic + wrong testcase: input is not list of lists as described in the problem description([fixed](https://github.com/evalplus/evalplus/commit/528d85a499419200dea5f07f7255993410ac30a0))
- *[109](109.py): redundant argument n as list len*
- [119](119.py): imprecise problem description: doesn't specify the sorting order
- [128](128.py): wrong testcase: the input is not list of words as described in the problem description
- [170](170.py): imprecise problem description: doesn't specify the `range` precisely as inclusive/exclusive/half-open, groundtruth implies inclusive range, (maybe LLMs can learn that from contracts?)
- *[223](223.py): imprecise problem description: doesn't specify the sorting order, though can be learned from testcase*
- [229](229.py): bad logic + wrong testcase
- [307](307.py): confusing problem
- [310](310.py): imprecise problem description: description itself doesn't require ignore space, but the groundtruth does 
- [391](391.py): imprecise problem description: doesn't specify list number in inputs and the output dict format
- *[393](393.py): duplicate problem: same as [290](290.py)*
- *[411](411.py): duplicate problem: same as [102](102.py)*
- [417](417.py): confusing problem: testcases have nothing to do with the problem description
- [443](443.py): confusing problem: according to the groundtruth, the 'largerst negative number' is the smallest negative number or 'negative number with largest absolute value'
- [452](452.py): bad logic + wrong testcase: impl and testcases seem to have understood the meaning of 'sales_amount' and 'actual_cost'
- [464](464.py): bad logic: groundtruth implments "all values equals to n', instead of 'all values are same' as the description
- [465](465.py): confusing problem: 'empty item' is not a well-defined concept
- *[556](556.py): redundant argument N as list len*
- *[559](559.py): redundant argument size as list len*
- *[559](564.py): redundant argument n as list len*
- *[584](584.py): duplicate problem: same as [440](440.py), but 584 has a better description*
- [603](603.py): problem description typo: 'lucid' => 'ludic'
- [617](617.py): wrong testcase + bad logic: the jump steps should be a integer
- *[622](622.py): redundant argument n as list len*
- *[625](625.py): same as [591](591.py)*
- [627](627.py): unclear arguments: start and end are ill-defined in the problem description, unclear without reading implementation
- [633](633.py): redundant argument n as list len*
### multi-solution problems
problems with multiple correct answers for certain inputs

- [119](119.py): consider `search([1, 2 ,3])`
- [130](130.py): testcase2: 7/8/9 are all correct answers
- [462](462.py): the order of each sublist is not important, so using '==' in testcases are not suitable
- [630](630.py): order issue same as [462](462.py)
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

from pathlib import Path

import pytest

import evalplus.eval as evaluator


@pytest.fixture(autouse=True)
def disable_memory_limit_on_test_child(monkeypatch):
    monkeypatch.setenv("EVALPLUS_MAX_MEMORY_BYTES", "-1")


def check(code, inputs, expected):
    return evaluator.untrusted_check(
        "mbpp",
        code,
        inputs,
        "cube_nums",
        expected,
        0,
        [0.01] * len(inputs),
        min_time_limit=2,
    )


def test_imports_checkout_source():
    assert Path(evaluator.__file__).resolve() == (
        Path(__file__).resolve().parents[1] / "evalplus/eval/__init__.py"
    )


@pytest.mark.parametrize("value", [[1, 0.5], (1, 0.5), [[1], [0.5]], [[], [1, 0.5]]])
def test_detects_floats_in_mixed_and_nested_values(value):
    assert evaluator.is_floats(value)


@pytest.mark.parametrize("value", [[], (), [1, 2], [[1], [2]], [[], []]])
def test_integer_and_empty_values_do_not_infer_float_tolerance(value):
    assert not evaluator.is_floats(value)


def test_correct_mixed_cube_output_is_not_rejected_for_one_ulp():
    nums = [1, 2.5, 3, -4.7, 5, 6, 7, -8.9]
    canonical = [n**3 for n in nums]
    candidate = [n * n * n for n in nums]
    assert canonical != candidate
    assert abs(canonical[3] - candidate[3]) < 1e-6
    status, details = check(
        "def cube_nums(nums): return [n*n*n for n in nums]",
        [(nums,)],
        [canonical],
    )
    assert status == evaluator.PASS
    assert details == [True]


@pytest.mark.parametrize("constructor", ["list", "tuple"])
def test_nested_mixed_outputs_allow_float_roundoff(constructor):
    status, details = check(
        f"def cube_nums(x): return {constructor}([1, [0.5 + 2e-7]])",
        [(0,)],
        [[1, [0.5]]] if constructor == "list" else [(1, [0.5])],
    )
    assert status == evaluator.PASS
    assert details == [True]


def test_integer_errors_inside_mixed_output_stay_exact():
    status, details = check(
        "def cube_nums(x): return [0.5, 10**9 + 50]",
        [(0,)],
        [[0.5, 10**9]],
    )
    assert status == evaluator.FAIL
    assert details == [False]


@pytest.mark.parametrize(
    "value", ["[0.5, [10**9 + 50]]", "[0.5, [1, 2, 3]]", "[0.5, 'wrong']"]
)
def test_nested_integer_shape_and_text_errors_still_fail(value):
    status, details = check(
        f"def cube_nums(x): return {value}",
        [(0,)],
        [[0.5, [10**9]]],
    )
    assert status == evaluator.FAIL
    assert details == [False]

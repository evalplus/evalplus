from pathlib import Path

import pytest

import evalplus.eval as evaluator


@pytest.fixture(autouse=True)
def disable_memory_limit_on_test_child(monkeypatch):
    # The package provides this option for platforms that cannot set RLIMIT_AS.
    monkeypatch.setenv("EVALPLUS_MAX_MEMORY_BYTES", "-1")


def run_case(code, inputs, expected, atol=0, dataset="humaneval", fast_check=False):
    return evaluator.untrusted_check(
        dataset=dataset,
        code=code,
        inputs=inputs,
        entry_point="solve",
        expected=expected,
        atol=atol,
        ref_time=[0.01] * len(inputs),
        min_time_limit=2,
        fast_check=fast_check,
    )


def test_imports_checkout_source():
    assert Path(evaluator.__file__).resolve() == (
        Path(__file__).resolve().parents[1] / "evalplus/eval/__init__.py"
    )


@pytest.mark.parametrize("dataset", ["humaneval", "mbpp"])
@pytest.mark.parametrize("fast_check", [False, True])
@pytest.mark.parametrize("values", [[0.5, 10**9], [10**9, 0.5]])
def test_integer_verdict_does_not_depend_on_an_earlier_float(
    dataset, fast_check, values
):
    status, details = run_case(
        "def solve(x): return x + 50 if isinstance(x, int) else x",
        [(x,) for x in values],
        values,
        dataset=dataset,
        fast_check=fast_check,
    )
    assert status == evaluator.FAIL
    if not fast_check:
        assert details == [not isinstance(x, int) for x in values]


@pytest.mark.parametrize("constructor", ["list", "tuple"])
def test_inferred_tolerance_does_not_leak_from_float_sequences(constructor):
    values = [[0.5], [10**9]] if constructor == "list" else [(0.5,), (10**9,)]
    status, details = run_case(
        f"def solve(x): return {constructor}([x[0] + 50]) if isinstance(x[0], int) else x",
        [(x,) for x in values],
        values,
    )
    assert status == evaluator.FAIL
    assert details == [True, False]


@pytest.mark.parametrize("values", [[0.5, 10**9], [10**9, 0.5]])
def test_inferred_float_tolerance_is_preserved(values):
    status, details = run_case(
        "def solve(x): return x + 2e-7 if isinstance(x, float) else x",
        [(x,) for x in values],
        values,
    )
    assert status == evaluator.PASS
    assert details == [True, True]


@pytest.mark.parametrize("values", [[0.5, 10**9], [10**9, 0.5]])
def test_explicit_tolerance_is_preserved(values):
    status, details = run_case(
        "def solve(x): return x + 50 if isinstance(x, int) else x",
        [(x,) for x in values],
        values,
        atol=1e-6,
    )
    assert status == evaluator.PASS
    assert details == [True, True]


def test_correct_mixed_outputs_still_pass():
    status, details = run_case(
        "def solve(x): return x",
        [(0.5,), (10**9,), ([0.5],), ([10**9],)],
        [0.5, 10**9, [0.5], [10**9]],
    )
    assert status == evaluator.PASS
    assert details == [True] * 4


def test_invalid_type_or_shape_still_fails():
    status, details = run_case(
        "def solve(x): return [x]",
        [(0.5,), (0.5,)],
        [0.5, [0.5, 0.5]],
    )
    assert status == evaluator.FAIL
    assert details == [False, False]

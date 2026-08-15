import math

from evalplus.uncertainty import paired_mcnemar, wilson_ci


def test_wilson_ci_center():
    lo, hi = wilson_ci(50, 100)
    assert abs((lo + hi) / 2 - 0.5) < 1e-9
    assert lo < 0.5 < hi


def test_wilson_ci_extreme():
    lo, hi = wilson_ci(0, 10)
    assert lo == 0.0
    lo, hi = wilson_ci(10, 10)
    assert hi == 1.0


def test_wilson_ci_reference():
    # Wilson 95% interval for 50/100 is (0.402, 0.598) to 3 decimals.
    lo, hi = wilson_ci(50, 100)
    assert abs(lo - 0.4038) < 0.001
    assert abs(hi - 0.5962) < 0.001


def test_mcnemar_classic():
    # The textbook (1, 9) discordant pair yields a two-sided p of ~0.0215.
    p = paired_mcnemar(1, 9)
    assert abs(p - 0.02148) < 0.0001


def test_mcnemar_no_discordance():
    assert paired_mcnemar(0, 0) == 1.0

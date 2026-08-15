"""Statistical helpers for comparing fixed-item evaluation results.

Implements the Wilson score interval for pass rates and an exact paired
McNemar test for comparing two models on the same fixed item set. Only the
standard library is required.
"""

from __future__ import annotations

import math


def wilson_ci(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Return the (lower, upper) Wilson score interval for a proportion.

    The Wilson interval is well behaved near 0 and 1, unlike the normal
    approximation, which makes it suitable for fixed-item leaderboards where
    pass rates are often extreme (e.g. 0.95 or 0.05).
    """
    if n <= 0:
        return (0.0, 0.0)
    p = successes / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, center - margin), min(1.0, center + margin))


def paired_mcnemar(a_only: int, b_only: int, two_sided: bool = True) -> float:
    """Exact binomial p-value for the paired McNemar test.

    ``a_only`` is the number of items solved by A but not B; ``b_only`` the
    reverse. Under the null hypothesis the discordant items split 50/50, so
    the test reduces to a binomial test on the smaller discordant count.
    """
    n = a_only + b_only
    if n == 0:
        return 1.0
    k = min(a_only, b_only)
    tail = 0.0
    for i in range(k + 1):
        tail += math.comb(n, i) / (2**n)
    return min(1.0, 2 * tail) if two_sided else tail

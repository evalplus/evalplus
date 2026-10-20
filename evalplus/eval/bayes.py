"""Binary Bayes@N posterior moments (https://arxiv.org/abs/2510.04265)."""

import math
from numbers import Integral
from typing import Dict, Sequence


def estimate_bayes_at_n(
    num_samples: Sequence[int], num_correct: Sequence[int]
) -> Dict[str, float]:
    """Return the posterior mean and SD of average task success probability.

    Each task has an independent Beta(1, 1) prior. Counts must describe a
    nonempty set of tasks with the same positive number of sampled programs.
    Historical observations and nonbinary rubrics are not supported here.
    """
    if len(num_samples) == 0 or len(num_samples) != len(num_correct):
        raise ValueError("Bayes@N needs matching, nonempty task counts")
    for n, c in zip(num_samples, num_correct):
        if (
            isinstance(n, bool)
            or isinstance(c, bool)
            or not isinstance(n, Integral)
            or not isinstance(c, Integral)
            or n <= 0
            or not 0 <= c <= n
        ):
            raise ValueError("Bayes@N needs integer counts with N > 0 and 0 <= c <= N")
    if any(n != num_samples[0] for n in num_samples):
        raise ValueError("Bayes@N needs the same number of samples for every task")

    total = int(num_samples[0]) + 2
    means = [(int(c) + 1) / total for c in num_correct]
    variances = [
        ((int(c) + 1) / total)
        * ((int(num_samples[0]) - int(c) + 1) / total)
        / (total + 1)
        for c in num_correct
    ]
    tasks = len(num_samples)
    return {
        "mean": math.fsum(means) / tasks,
        "std": math.sqrt(math.fsum(variances)) / tasks,
    }

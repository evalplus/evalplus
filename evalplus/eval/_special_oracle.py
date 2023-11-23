"""Special oracle handlings for problems where direct differential testing is not applicable."""
import math

# For tasks whose output are not serializable, we only check the output is not None, which
# is also consistent with the original dataset.
MBPP_OUTPUT_NOT_NONE_TASKS = ["check_str", "text_match_three", "text_starta_endb"]


# oracle for HumaneEval/032
def _poly(xs: list, x: float):
    """
    Evaluates polynomial with coefficients xs at point x.
    return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n
    """
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])

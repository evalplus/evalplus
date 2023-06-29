"""
Write a function to find the ratio of zeroes to non-zeroes in an array of integers.
"""

from array import array
def zero_count(nums):
    assert isinstance(nums, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, (int, float)) for x in nums), "invalid inputs" # $_CONTRACT_$
    assert len(nums) > 0, "invalid inputs" # $_CONTRACT_$
    n = len(nums)
    n1 = 0
    for x in nums:
        if x == 0:
            n1 += 1
        else:
          None
    return n1/(n-n1)

import math

assert math.isclose(zero_count([0, 1, 2, -1, -5, 6, 0, -3, -2, 3, 4, 6, 8]), 0.181818, rel_tol=0.001)
assert math.isclose(zero_count([2, 1, 2, -1, -5, 6, 4, -3, -2, 3, 4, 6, 8]), 0.00, rel_tol=0.001)
assert math.isclose(zero_count([2, 4, -6, -9, 11, -12, 14, -5, 17]), 0.00, rel_tol=0.001)

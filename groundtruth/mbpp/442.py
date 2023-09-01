"""
Write a function to find the ration of positive numbers in an array of integers.
"""

def positive_count(nums):
    assert isinstance(nums, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(ele, int) for ele in nums), "invalid inputs" # $_CONTRACT_$
    assert len(nums) > 0, "invalid inputs" # $_CONTRACT_$
    return sum(x > 0 for x in nums) / len(nums)

import math
assert math.isclose(positive_count([0, 1, 2, -1, -5, 6, 0, -3, -2, 3, 4, 6, 8]), 0.538, rel_tol=0.001)
assert math.isclose(positive_count([2, 1, 2, -1, -5, 6, 4, -3, -2, 3, 4, 6, 8]), 0.692, rel_tol=0.001)
assert math.isclose(positive_count([2, 4, -6, -9, 11, -12, 14, -5, 17]), 0.555, rel_tol=0.001)

"""
Write a function to convert a given tuple of positive integers into a single integer.
"""

def tuple_to_int(nums):
    assert isinstance(nums, tuple), "invalid inputs" # $_CONTRACT_$
    assert len(nums) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, int) for x in nums), "invalid inputs" # $_CONTRACT_$
    assert all(x > 0 for x in nums), "invalid inputs" # $_CONTRACT_$
    return int(''.join(map(str,nums)))



assert tuple_to_int((1,2,3))==123
assert tuple_to_int((4,5,6))==456
assert tuple_to_int((5,6,7))==567

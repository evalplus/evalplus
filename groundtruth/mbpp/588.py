"""
Write a python function to find the difference between largest and smallest value in a given list.
"""

def big_diff(nums):
     assert isinstance(nums, list), "invalid inputs" # $_CONTRACT_$
     assert len(nums) > 0, "invalid inputs" # $_CONTRACT_$
     assert all(isinstance(x, (int, float)) for x in nums), "invalid inputs" # $_CONTRACT_$
     return max(nums) - min(nums)



assert big_diff([1,2,3,4]) == 3
assert big_diff([4,5,12]) == 8
assert big_diff([9,2,3]) == 7

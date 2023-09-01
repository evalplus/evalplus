"""
Write a python function to find the sum of the largest and smallest value in a given array.
"""

def big_sum(nums):
      assert isinstance(nums, list), "invalid inputs" # $_CONTRACT_$
      assert len(nums) > 0, "invalid inputs" # $_CONTRACT_$
      assert all(isinstance(n, (int, float)) for n in nums), "invalid inputs" # $_CONTRACT_$
      return max(nums) + min(nums)



assert big_sum([1,2,3]) == 4
assert big_sum([-1,2,3,4]) == 3
assert big_sum([2,3,6]) == 8

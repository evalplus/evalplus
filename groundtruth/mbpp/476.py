"""
Write a python function to find the sum of the largest and smallest value in a given array.
"""

def big_sum(nums):
      sum= max(nums)+min(nums)
      return sum



assert big_sum([1,2,3]) == 4
assert big_sum([-1,2,3,4]) == 3
assert big_sum([2,3,6]) == 8

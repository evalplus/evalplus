"""
Write a python function to remove duplicate numbers from a given number of lists.
"""

def two_unique_nums(nums):
  assert isinstance(nums, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, (int, float)) for x in nums), "invalid inputs" # $_CONTRACT_$
  return [i for i in nums if nums.count(i)==1]



assert two_unique_nums([1,2,3,2,3,4,5]) == [1, 4, 5]
assert two_unique_nums([1,2,3,2,4,5]) == [1, 3, 4, 5]
assert two_unique_nums([1,2,3,4,5]) == [1, 2, 3, 4, 5]

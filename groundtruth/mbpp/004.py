"""
Write a function to find the n largest integers from a given list of numbers, returned in descending order.
"""

import heapq as hq
def heap_queue_largest(nums: list,n: int) -> list:
  assert isinstance(nums, list), "invalid inputs" # $_CONTRACT_$
  assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
  assert n > 0, "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(i, (int, float)) for i in nums), "invalid inputs" # $_CONTRACT_$
  largest_nums = hq.nlargest(n, nums)
  return largest_nums



assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],3)==[85, 75, 65]
assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],2)==[85, 75]
assert heap_queue_largest( [25, 35, 22, 85, 14, 65, 75, 22, 58],5)==[85, 75, 65, 58, 35]

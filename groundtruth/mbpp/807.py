"""
Write a python function to find the first odd number in a given list of numbers.
"""

def first_odd(nums):
  assert isinstance(nums, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(el, int) for el in nums), "invalid inputs" # $_CONTRACT_$
  assert any(el % 2 != 0 for el in nums), "invalid inputs" # $_CONTRACT_$
  first_odd = next((el for el in nums if el%2!=0), None)
  return first_odd



assert first_odd([1,3,5]) == 1
assert first_odd([2,4,1,3]) == 1
assert first_odd ([8,9,1]) == 9

"""
Write a python function to find the first odd number in a given list of numbers.
"""

def first_odd(nums):
  first_odd = next((el for el in nums if el%2!=0),-1)
  return first_odd



assert first_odd([1,3,5]) == 1
assert first_odd([2,4,1,3]) == 1
assert first_odd ([8,9,1]) == 9

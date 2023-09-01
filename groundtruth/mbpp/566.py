"""
Write a function to get the sum of the digits of a non-negative integer.
"""

def sum_digits(n):
  assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
  assert n >= 0, "invalid inputs" # $_CONTRACT_$
  return sum(map(int, str(n)))



assert sum_digits(345)==12
assert sum_digits(12)==3
assert sum_digits(97)==16

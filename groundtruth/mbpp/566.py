"""
Write a function to get the sum of the digits of a non-negative integer.
"""

def sum_digits(n):
  assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
  assert n >= 0, "invalid inputs" # $_CONTRACT_$
  if n == 0:
    return 0
  else:
    return n % 10 + sum_digits(int(n / 10))



assert sum_digits(345)==12
assert sum_digits(12)==3
assert sum_digits(97)==16

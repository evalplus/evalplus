"""
Write a python function to find the number of divisors of a given integer.
"""

def divisor(n):
  assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
  assert n > 0, "invalid inputs" # $_CONTRACT_$
  return sum(1 for i in range(1, n + 1) if n % i == 0)



assert divisor(15) == 4
assert divisor(12) == 6
assert divisor(9) == 3

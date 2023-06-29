"""
Write a python function to find the number of divisors of a given integer.
"""

def divisor(n):
  assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
  assert n > 0, "invalid inputs" # $_CONTRACT_$
  for i in range(n):
    x = len([i for i in range(1,n+1) if not n % i])
  return x



assert divisor(15) == 4
assert divisor(12) == 6
assert divisor(9) == 3

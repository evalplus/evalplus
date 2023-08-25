"""
Write a function that takes in an integer n and calculates the harmonic sum of n-1.
"""

def harmonic_sum(n):
  assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
  assert n >= 1, "invalid inputs" # $_CONTRACT_$
  return sum(1/(i + 1) for i in range(n))

import math

assert math.isclose(harmonic_sum(7), 2.5928571428571425, rel_tol=0.001)
assert math.isclose(harmonic_sum(4), 2.083333333333333, rel_tol=0.001)
assert math.isclose(harmonic_sum(19), 3.547739657143682, rel_tol=0.001)

"""
Write a function that takes in an integer n and calculates the harmonic sum of n-1.
"""

def harmonic_sum(n):
  assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
  if n < 2:
    return 1
  else:
    return 1 / n + (harmonic_sum(n - 1)) 

import math

assert math.isclose(harmonic_sum(7), 2.5928571428571425, rel_tol=0.001)
assert math.isclose(harmonic_sum(4), 2.083333333333333, rel_tol=0.001)
assert math.isclose(harmonic_sum(19), 3.547739657143682, rel_tol=0.001)

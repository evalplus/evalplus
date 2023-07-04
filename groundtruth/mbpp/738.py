"""
Write a function to calculate the geometric sum of n-1. https://www.w3resource.com/python-exercises/data-structures-and-algorithms/python-recursion-exercise-9.php
"""

def geometric_sum(n):
  assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
  if n < 0:
    return 0
  else:
    return 1 / (pow(2, n)) + geometric_sum(n - 1)



assert geometric_sum(7) == 1.9921875
assert geometric_sum(4) == 1.9375
assert geometric_sum(8) == 1.99609375

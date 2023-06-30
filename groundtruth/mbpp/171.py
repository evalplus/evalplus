"""
Write a function to find the perimeter of a regular pentagon from the length of its sides.
"""

import math
def perimeter_pentagon(a):
  assert isinstance(a, (int, float)), "invalid inputs" # $_CONTRACT_$
  perimeter=(5*a)
  return perimeter



assert perimeter_pentagon(5) == 25
assert perimeter_pentagon(10) == 50
assert perimeter_pentagon(15) == 75

"""
Write a function to calculate the area of a regular polygon given the length and number of its sides.
"""

from math import tan, pi
def area_polygon(s, l):
  assert isinstance(s, int), "invalid inputs" # $_CONTRACT_$
  assert isinstance(l, int), "invalid inputs" # $_CONTRACT_$
  assert s > 0, "invalid inputs" # $_CONTRACT_$
  assert l > 0, "invalid inputs" # $_CONTRACT_$
  area = s * (l ** 2) / (4 * tan(pi / s))
  return area

import math

assert math.isclose(area_polygon(4, 20), 400., rel_tol=0.001)
assert math.isclose(area_polygon(10, 15), 1731.197, rel_tol=0.001)
assert math.isclose(area_polygon(9, 7), 302.909, rel_tol=0.001)

"""
Write a function to find the lateral surface area of a cylinder.
"""

import math
def lateralsuface_cylinder(r, h):
  assert isinstance(r, (int, float)), "invalid inputs" # $_CONTRACT_$
  assert isinstance(h, (int, float)), "invalid inputs" # $_CONTRACT_$
  assert r > 0, "invalid inputs" # $_CONTRACT_$
  assert h > 0, "invalid inputs" # $_CONTRACT_$
  return 2 * math.pi * r * h

import math

assert math.isclose(lateralsuface_cylinder(10,5), 314.15000000000003, rel_tol=0.001)
assert math.isclose(lateralsuface_cylinder(4,5), 125.66000000000001, rel_tol=0.001)
assert math.isclose(lateralsuface_cylinder(4,10), 251.32000000000002, rel_tol=0.001)

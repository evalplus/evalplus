"""
Write a function that takes in the radius and height of a cylinder and returns the the volume.
"""

import math
def volume_cylinder(r,h):
  assert isinstance(r, (int, float)), "invalid inputs" # $_CONTRACT_$
  assert isinstance(h, (int, float)), "invalid inputs" # $_CONTRACT_$
  assert r > 0, "invalid inputs" # $_CONTRACT_$
  assert h > 0, "invalid inputs" # $_CONTRACT_$
  return math.pi * r * r * h

import math

assert math.isclose(volume_cylinder(10,5), 1570.7500000000002, rel_tol=0.001)
assert math.isclose(volume_cylinder(4,5), 251.32000000000002, rel_tol=0.001)
assert math.isclose(volume_cylinder(4,10), 502.64000000000004, rel_tol=0.001)

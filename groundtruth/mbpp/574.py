"""
Write a function to find the surface area of a cylinder.
"""

from math import pi
def surfacearea_cylinder(r,h):
  assert isinstance(r, int), "invalid inputs" # $_CONTRACT_$
  assert isinstance(h, int), "invalid inputs" # $_CONTRACT_$
  assert r > 0, "invalid inputs" # $_CONTRACT_$
  assert h > 0, "invalid inputs" # $_CONTRACT_$
  return (2*pi*r*r) + (2*pi*r*h)



import math
assert math.isclose(surfacearea_cylinder(10,5), 942.45, rel_tol=0.001)
assert math.isclose(surfacearea_cylinder(4,5), 226.18800000000002, rel_tol=0.001)
assert math.isclose(surfacearea_cylinder(4,10), 351.848, rel_tol=0.001)

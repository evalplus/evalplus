"""
Write a function to find the volume of a cone.
"""

import math
def volume_cone(r,h):
  assert isinstance(r, (int, float)) and r > 0, "invalid inputs" # $_CONTRACT_$
  return (1.0 / 3) * math.pi * r * r * h

import math

assert math.isclose(volume_cone(5,12), 314.15926535897927, rel_tol=0.001)
assert math.isclose(volume_cone(10,15), 1570.7963267948965, rel_tol=0.001)
assert math.isclose(volume_cone(19,17), 6426.651371693521, rel_tol=0.001)

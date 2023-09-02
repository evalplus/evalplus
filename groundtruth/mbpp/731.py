"""
Write a function to find the lateral surface area of a cone given radius r and the height h.
"""

import math
def lateralsurface_cone(r,h):
  assert isinstance(r, (int, float)), "invalid inputs" # $_CONTRACT_$
  assert isinstance(h, (int, float)), "invalid inputs" # $_CONTRACT_$
  assert r > 0, "invalid inputs" # $_CONTRACT_$
  assert h > 0, "invalid inputs" # $_CONTRACT_$
  l = math.sqrt(r * r + h * h)
  return math.pi * r  * l



assert lateralsurface_cone(5,12)==204.20352248333654
assert lateralsurface_cone(10,15)==566.3586699569488
assert lateralsurface_cone(19,17)==1521.8090132193388

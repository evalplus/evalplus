"""
Write a function to find the lateral surface area of a cone given radius r and the height h.
"""

import math
def lateralsurface_cone(r,h):
  l = math.sqrt(r * r + h * h)
  LSA = math.pi * r  * l
  return LSA



assert lateralsurface_cone(5,12)==204.20352248333654
assert lateralsurface_cone(10,15)==566.3586699569488
assert lateralsurface_cone(19,17)==1521.8090132193388

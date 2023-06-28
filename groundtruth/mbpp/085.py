"""
Write a function to find the surface area of a sphere.
"""

import math
def surfacearea_sphere(r):
  surfacearea=4*math.pi*r*r
  return surfacearea

import math

assert math.isclose(surfacearea_sphere(10), 1256.6370614359173, rel_tol=0.001)
assert math.isclose(surfacearea_sphere(15), 2827.4333882308138, rel_tol=0.001)
assert math.isclose(surfacearea_sphere(20), 5026.548245743669, rel_tol=0.001)

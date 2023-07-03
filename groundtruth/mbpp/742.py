"""
Write a function to caluclate the area of a tetrahedron.
"""

import math
def area_tetrahedron(side):
  assert isinstance(side, (int, float)), "invalid inputs" # $_CONTRACT_$
  assert side > 0, "invalid inputs" # $_CONTRACT_$
  area = math.sqrt(3)*(side*side)
  return area



assert area_tetrahedron(3)==15.588457268119894
assert area_tetrahedron(20)==692.8203230275509
assert area_tetrahedron(10)==173.20508075688772

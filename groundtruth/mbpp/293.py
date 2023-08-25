"""
Write a function to find the third side of a right angled triangle.
"""

import math
def otherside_rightangle(w,h):
  assert isinstance(w, (int, float)) and w > 0, "invalid inputs" # $_CONTRACT_$
  assert isinstance(h, (int, float)) and h > 0, "invalid inputs" # $_CONTRACT_$
  return math.sqrt(w * w + h * h)



import math
assert math.isclose(otherside_rightangle(7,8), 10.63014581273465, rel_tol=0.001)
assert math.isclose(otherside_rightangle(3,4), 5, rel_tol=0.001)
assert math.isclose(otherside_rightangle(7,15), 16.55294535724685, rel_tol=0.001)

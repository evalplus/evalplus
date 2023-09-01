"""
Write a function to find the area of a rectangle.
"""

def rectangle_area(l,b):
  assert isinstance(l, (int, float)), "invalid inputs" # $_CONTRACT_$
  assert isinstance(b, (int, float)), "invalid inputs" # $_CONTRACT_$
  assert l > 0, "invalid inputs" # $_CONTRACT_$
  assert b > 0, "invalid inputs" # $_CONTRACT_$
  return l * b



assert rectangle_area(10,20)==200
assert rectangle_area(10,5)==50
assert rectangle_area(4,2)==8

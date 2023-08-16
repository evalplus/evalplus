"""
Write a function that returns the perimeter of a square given its side length as input.
"""

def square_perimeter(a):
  assert isinstance(a, (int, float)), "invalid inputs" # $_CONTRACT_$
  assert a > 0, "invalid inputs" # $_CONTRACT_$
  return 4*a



assert square_perimeter(10)==40
assert square_perimeter(5)==20
assert square_perimeter(4)==16

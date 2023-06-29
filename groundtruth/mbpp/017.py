"""
Write a function that returns the perimeter of a square given its side length as input.
"""

def square_perimeter(a):
  assert isinstance(a, (int, float)), "invalid inputs" # $_CONTRACT_$
  perimeter=4*a
  return perimeter



assert square_perimeter(10)==40
assert square_perimeter(5)==20
assert square_perimeter(4)==16

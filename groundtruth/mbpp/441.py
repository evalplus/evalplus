"""
Write a function to find the surface area of a cube of a given size.
"""

def surfacearea_cube(l):
  assert isinstance(l, (int, float)), "invalid inputs" # $_CONTRACT_$
  return 6 * l * l



assert surfacearea_cube(5)==150
assert surfacearea_cube(3)==54
assert surfacearea_cube(10)==600

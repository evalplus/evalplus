"""
Write a function to find the lateral surface area of a cube given its side length.
"""

def lateralsurface_cube(l):
  assert isinstance(l, (int, float)), "invalid inputs" # $_CONTRACT_$
  LSA = 4 * (l * l)
  return LSA



assert lateralsurface_cube(5)==100
assert lateralsurface_cube(9)==324
assert lateralsurface_cube(10)==400

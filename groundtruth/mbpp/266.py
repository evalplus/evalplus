"""
Write a function to find the lateral surface area of a cube given its side length.
"""

def lateralsurface_cube(l):
  assert isinstance(l, (int, float)), "invalid inputs" # $_CONTRACT_$
  assert l > 0, "invalid inputs" # $_CONTRACT_$
  return 4 * l * l



assert lateralsurface_cube(5)==100
assert lateralsurface_cube(9)==324
assert lateralsurface_cube(10)==400

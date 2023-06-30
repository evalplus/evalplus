"""
Write a function to find the volume of a cube given its side length.
"""

def volume_cube(l):
  assert isinstance(l, (int, float)), "invalid inputs" # $_CONTRACT_$
  volume = l * l * l
  return volume



assert volume_cube(3)==27
assert volume_cube(2)==8
assert volume_cube(5)==125

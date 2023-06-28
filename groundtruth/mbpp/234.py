"""
Write a function to find the volume of a cube given its side length.
"""

def volume_cube(l):
  volume = l * l * l
  return volume



assert volume_cube(3)==27
assert volume_cube(2)==8
assert volume_cube(5)==125

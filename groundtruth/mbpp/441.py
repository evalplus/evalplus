"""
Write a function to find the surface area of a cube of a given size.
"""

def surfacearea_cube(l):
  surfacearea= 6*l*l
  return surfacearea



assert surfacearea_cube(5)==150
assert surfacearea_cube(3)==54
assert surfacearea_cube(10)==600

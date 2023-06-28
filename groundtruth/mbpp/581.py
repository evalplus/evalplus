"""
Write a python function to find the surface area of a square pyramid with a given base edge and height.
"""

def surface_Area(b,s): 
    return 2 * b * s + pow(b,2) 



assert surface_Area(3,4) == 33
assert surface_Area(4,5) == 56
assert surface_Area(1,2) == 5

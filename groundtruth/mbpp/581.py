"""
Write a python function to find the surface area of a square pyramid with a given base edge and height.
"""

def surface_Area(b,s): 
    assert isinstance(b, (int, float)), "invalid inputs" # $_CONTRACT_$
    assert isinstance(s, (int, float)), "invalid inputs" # $_CONTRACT_$
    assert b >= 0, "invalid inputs" # $_CONTRACT_$
    assert s >= 0, "invalid inputs" # $_CONTRACT_$
    return 2 * b * s + pow(b,2) 



assert surface_Area(3,4) == 33
assert surface_Area(4,5) == 56
assert surface_Area(1,2) == 5

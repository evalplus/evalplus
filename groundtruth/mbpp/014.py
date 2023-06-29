"""
Write a python function to find the volume of a triangular prism.
"""

def find_Volume(l,b,h) : 
    assert isinstance(l, (int, float)), "invalid inputs" # $_CONTRACT_$
    assert isinstance(b, (int, float)), "invalid inputs" # $_CONTRACT_$
    assert isinstance(h, (int, float)), "invalid inputs" # $_CONTRACT_$
    assert l > 0, "invalid inputs" # $_CONTRACT_$
    assert b > 0, "invalid inputs" # $_CONTRACT_$
    assert h > 0, "invalid inputs" # $_CONTRACT_$
    return ((l * b * h) / 2) 



assert find_Volume(10,8,6) == 240
assert find_Volume(3,2,2) == 6
assert find_Volume(1,2,1) == 1

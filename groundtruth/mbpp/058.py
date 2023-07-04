"""
Write a python function to check whether the given two integers have opposite sign or not.
"""

def opposite_Signs(x,y): 
    assert isinstance(x, int), "invalid inputs" # $_CONTRACT_$
    assert isinstance(y, int), "invalid inputs" # $_CONTRACT_$
    assert x != 0 and y != 0, "invalid inputs" # $_CONTRACT_$
    return ((x ^ y) < 0); 



assert opposite_Signs(1,-2) == True
assert opposite_Signs(3,2) == False
assert opposite_Signs(-10,-10) == False
assert opposite_Signs(-2,2) == True

"""
Write a python function to find the area of the largest triangle that can be inscribed in a semicircle with a given radius.
"""

def triangle_area(r) :  
    assert isinstance(r, (int, float)), "invalid inputs" # $_CONTRACT_$
    if r < 0 : 
        return None
    return r * r 



assert triangle_area(-1) == None
assert triangle_area(0) == 0
assert triangle_area(2) == 4

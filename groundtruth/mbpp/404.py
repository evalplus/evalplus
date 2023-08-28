"""
Write a python function to find the minimum of two numbers.
"""

def minimum(a,b):   
    assert isinstance(a, (int, float)), "invalid inputs" # $_CONTRACT_$
    assert isinstance(b, (int, float)), "invalid inputs" # $_CONTRACT_$ 
    return min(a,b)



assert minimum(1,2) == 1
assert minimum(-5,-4) == -5
assert minimum(0,0) == 0

"""
Write a python function to find the maximum of two numbers.
"""

def maximum(a,b):   
    assert isinstance(a, (int, float)), "invalid inputs" # $_CONTRACT_$
    assert isinstance(b, (int, float)), "invalid inputs" # $_CONTRACT_$
    return max(a, b)



assert maximum(5,10) == 10
assert maximum(-1,-2) == -1
assert maximum(9,7) == 9

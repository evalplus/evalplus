"""
Write a python function to find quotient of two numbers (rounded down to the nearest integer).
"""

def find(n,m):  
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert isinstance(m, int), "invalid inputs" # $_CONTRACT_$
    assert m != 0, "invalid inputs" # $_CONTRACT_$
    return n // m 



assert find(10,3) == 3
assert find(4,2) == 2
assert find(20,5) == 4

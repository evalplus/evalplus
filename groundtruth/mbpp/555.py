"""
Write a python function to find the difference between the sum of cubes of the first n natural numbers and the sum of the first n natural numbers.
"""

def difference(n) :  
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    S = (n*(n + 1))//2;  
    res = S*(S-1);  
    return res;  



assert difference(3) == 30
assert difference(5) == 210
assert difference(2) == 6

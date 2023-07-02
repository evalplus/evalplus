"""
Write a python function to check whether the given number is even or not.
"""

def is_Even(n) : 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n > 0, "invalid inputs" # $_CONTRACT_$
    if (n^1 == n+1) :
        return True; 
    else :
        return False; 



assert is_Even(1) == False
assert is_Even(2) == True
assert is_Even(3) == False

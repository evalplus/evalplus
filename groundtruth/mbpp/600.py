"""
Write a python function to check whether the given number is even or not.
"""

def is_Even(n) : 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    return n % 2 == 0



assert is_Even(1) == False
assert is_Even(2) == True
assert is_Even(3) == False

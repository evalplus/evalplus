"""
Write a python function to find whether the parity of a given number is odd.
"""

def find_Parity(x): 
    assert isinstance(x, int), "invalid inputs" # $_CONTRACT_$
    return x % 2 != 0



assert find_Parity(12) == False
assert find_Parity(7) == True
assert find_Parity(10) == False

"""
Write a python function to find whether a number is divisible by 11.
"""

def is_Diff(n): 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    return (n % 11 == 0) 



assert is_Diff (12345) == False
assert is_Diff(1212112) == True
assert is_Diff(1212) == False

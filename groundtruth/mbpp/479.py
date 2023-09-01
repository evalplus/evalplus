"""
Write a python function to find the first digit of a given number.
"""

def first_Digit(n) :  
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    return int(str(n)[0])




assert first_Digit(123) == 1
assert first_Digit(456) == 4
assert first_Digit(12) == 1

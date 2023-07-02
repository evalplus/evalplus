"""
Write a python function to find the first digit of a given number.
"""

def first_Digit(n) :  
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    while n >= 10:  
        n = n / 10 
    return int(n) 



assert first_Digit(123) == 1
assert first_Digit(456) == 4
assert first_Digit(12) == 1

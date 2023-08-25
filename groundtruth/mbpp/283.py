"""
Write a python function takes in an integer and check whether the frequency of each digit in the integer is less than or equal to the digit itself.
"""

def validate(n): 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    digits = [int(digit) for digit in str(n)]
    return all(digit >= digits.count(digit) for digit in digits)



assert validate(1234) == True
assert validate(51241) == False
assert validate(321) == True

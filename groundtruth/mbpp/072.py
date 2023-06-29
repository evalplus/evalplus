"""
Write a python function to check whether the given number can be represented as the difference of two squares or not.
"""

def dif_Square(n): 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n > 0, "invalid inputs" # $_CONTRACT_$
    if (n % 4 != 2): 
        return True
    return False



assert dif_Square(5) == True
assert dif_Square(10) == False
assert dif_Square(15) == True

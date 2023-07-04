"""
Write a function to multiply all the numbers in a list and divide with the length of the list.
"""

def multiply_num(numbers):  
    assert isinstance(numbers, (tuple, list)), "invalid inputs" # $_CONTRACT_$
    assert len(numbers) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(item, (int, float)) for item in numbers), "invalid inputs" # $_CONTRACT_$
    total = 1
    for x in numbers:
        total *= x  
    return total/len(numbers) 

import math

assert math.isclose(multiply_num((8, 2, 3, -1, 7)), -67.2, rel_tol=0.001)
assert math.isclose(multiply_num((-10,-20,-30)), -2000.0, rel_tol=0.001)
assert math.isclose(multiply_num((19,15,18)), 1710.0, rel_tol=0.001)

"""
Write a python function to find the next perfect square greater than a given number.
"""

import math  
def next_Perfect_Square(N): 
    assert isinstance(N, (int, float)), "invalid inputs" # $_CONTRACT_$
    if N < 0:
        return 0
    nextN = math.floor(math.sqrt(N)) + 1
    return nextN * nextN 



assert next_Perfect_Square(35) == 36
assert next_Perfect_Square(6) == 9
assert next_Perfect_Square(9) == 16

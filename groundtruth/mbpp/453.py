"""
Write a python function to find the sum of even factors of a number.
"""

import math 
def sumofFactors(n) : 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    if (n % 2 != 0) : 
        return 0
    return sum([i for i in range(2, n + 1) if n % i == 0 and i % 2 == 0])



assert sumofFactors(18) == 26
assert sumofFactors(30) == 48
assert sumofFactors(6) == 8

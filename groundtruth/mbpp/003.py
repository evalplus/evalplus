"""
Write a python function to identify non-prime numbers.
"""

import math
def is_not_prime(n):
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n > 0, "invalid inputs" # $_CONTRACT_$
    if n == 1:
        return True
    for i in range(2, int(math.sqrt(n))+1):
        if n % i == 0:
            return True
    return False



assert is_not_prime(1) == True
assert is_not_prime(2) == False
assert is_not_prime(10) == True
assert is_not_prime(35) == True
assert is_not_prime(37) == False

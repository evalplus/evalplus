"""
Write a python function to find the sum of common divisors of two given numbers.
"""

import math
def sum(a,b): 
    assert isinstance(a, int), "invalid inputs" # $_CONTRACT_$
    assert isinstance(b, int), "invalid inputs" # $_CONTRACT_$
    assert a > 0, "invalid inputs" # $_CONTRACT_$
    assert b > 0, "invalid inputs" # $_CONTRACT_$
    sum = 0
    n = math.gcd(a, b)
    N = int(math.sqrt(n)) + 1
    for i in range (1, N): 
        if (n % i == 0): 
            sum += i
            if (n / i != i): 
                sum += (n / i)
    return sum



assert sum(10,15) == 6
assert sum(100,150) == 93
assert sum(4,6) == 3

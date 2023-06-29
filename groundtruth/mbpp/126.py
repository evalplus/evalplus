"""
Write a python function to find the sum of common divisors of two given numbers.
"""

def sum(a,b): 
    assert isinstance(a, int), "invalid inputs" # $_CONTRACT_$
    assert isinstance(b, int), "invalid inputs" # $_CONTRACT_$
    assert a > 0, "invalid inputs" # $_CONTRACT_$
    assert b > 0, "invalid inputs" # $_CONTRACT_$
    sum = 0
    for i in range (1,min(a,b)): 
        if (a % i == 0 and b % i == 0): 
            sum += i 
    return sum



assert sum(10,15) == 6
assert sum(100,150) == 93
assert sum(4,6) == 3

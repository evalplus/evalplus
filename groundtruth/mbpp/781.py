"""
Write a python function to check whether the count of divisors is even. https://www.w3resource.com/python-exercises/basic/python-basic-1-exercise-24.php
"""

import math 
def count_divisors(n) : 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n > 0, "invalid inputs" # $_CONTRACT_$
    count = 0
    for i in range(1, (int)(math.sqrt(n)) + 2) : 
        if (n % i == 0) : 
            if( n // i == i) : 
                count = count + 1
            else : 
                count = count + 2
    return count % 2 == 0



assert count_divisors(10)
assert not count_divisors(100)
assert count_divisors(125)

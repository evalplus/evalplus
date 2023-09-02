"""
Write a python function to check whether the count of divisors is even. https://www.w3resource.com/python-exercises/basic/python-basic-1-exercise-24.php
"""

import math 
def count_divisors(n) : 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n > 0, "invalid inputs" # $_CONTRACT_$
    cnt = 0
    for i in range(1, (int)(math.sqrt(n)) + 1) : 
        if (n % i == 0) : 
            if (n / i == i) : 
                cnt = cnt + 1
            else : 
                cnt = cnt + 2
    return cnt % 2 == 0



assert count_divisors(10)
assert not count_divisors(100)
assert count_divisors(125)

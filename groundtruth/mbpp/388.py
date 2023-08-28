"""
Write a python function to find the highest power of 2 that is less than or equal to n.
"""

def highest_Power_of_2(n): 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n > 0, "invalid inputs" # $_CONTRACT_$
    i = 0
    while ((1 << i) <= n): 
        i += 1
    return (1 << (i - 1))




assert highest_Power_of_2(10) == 8
assert highest_Power_of_2(19) == 16
assert highest_Power_of_2(32) == 32

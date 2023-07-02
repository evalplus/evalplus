"""
Write a python function to find the highest power of 2 that is less than or equal to n.
"""

def highest_Power_of_2(n): 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    res = 0 
    for i in range(n, 0, -1): 
        if ((i & (i - 1)) == 0): 
            res = i 
            break 
    return res 



assert highest_Power_of_2(10) == 8
assert highest_Power_of_2(19) == 16
assert highest_Power_of_2(32) == 32

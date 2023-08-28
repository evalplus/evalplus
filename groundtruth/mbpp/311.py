"""
Write a python function to set the left most unset bit.
"""

def set_left_most_unset_bit(n): 
    assert isinstance(n, int) and n >= 0, "invalid inputs" # $_CONTRACT_$
    if not (n & (n + 1)): 
        return n 
    pos, temp, count = 0, n, 0 
    while temp: 
        if not (temp & 1): 
            pos = count      
        count += 1
        temp >>= 1
    return (n | (1 << (pos))) 



assert set_left_most_unset_bit(10) == 14
assert set_left_most_unset_bit(12) == 14
assert set_left_most_unset_bit(15) == 15

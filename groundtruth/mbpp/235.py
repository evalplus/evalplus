"""
Write a python function to set all even bits of a given number.
"""

def even_bit_set_number(n): 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    mask = 2
    while mask < n:
        n |= mask
        mask <<= 2
    return n



assert even_bit_set_number(10) == 10
assert even_bit_set_number(20) == 30
assert even_bit_set_number(30) == 30

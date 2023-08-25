"""
Write a python function to count the number of set bits (binary digits with value 1) in a given number.
"""

def count_Set_Bits(n): 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    return bin(n)[2:].count('1')



assert count_Set_Bits(2) == 1
assert count_Set_Bits(4) == 1
assert count_Set_Bits(6) == 2

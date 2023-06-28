"""
Write a function to that rotate left bits by d bits a given number. We assume that the number is 32 bit.
"""

def left_rotate(n,d):   
    INT_BITS = 32
    return (n << d)|(n >> (INT_BITS - d))  



assert left_rotate(16,2) == 64
assert left_rotate(10,2) == 40
assert left_rotate(99,3) == 792
assert left_rotate(99,3) == 792
assert left_rotate(0b0001,3) == 0b1000
assert left_rotate(0b0101,3) == 0b101000
assert left_rotate(0b11101,3) == 0b11101000

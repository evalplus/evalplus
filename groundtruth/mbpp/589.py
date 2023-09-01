"""
Write a function to find perfect squares between two given numbers.
"""

import math
def perfect_squares(a, b):
    assert isinstance(a, int), "invalid inputs" # $_CONTRACT_$
    assert isinstance(b, int), "invalid inputs" # $_CONTRACT_$
    if a > b:
        a, b = b, a
    if b < 0:
        return []
    if a < 0:
        a = 0
    return list(filter(lambda x: math.sqrt(x).is_integer(), range(a, b+1)))



assert perfect_squares(1,30)==[1, 4, 9, 16, 25]
assert perfect_squares(50,100)==[64, 81, 100]
assert perfect_squares(100,200)==[100, 121, 144, 169, 196]

"""
Write a function to multiply two integers.
"""

def multiply_int(x, y):
    assert isinstance(x, int), "invalid inputs" # $_CONTRACT_$
    assert isinstance(y, int), "invalid inputs" # $_CONTRACT_$
    return x * y



assert multiply_int(10,20)==200
assert multiply_int(5,10)==50
assert multiply_int(4,8)==32

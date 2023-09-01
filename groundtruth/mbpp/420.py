"""
Write a python function to find the cube sum of first n even natural numbers.
"""

def cube_Sum(n): 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    return 2 * (n ** 2) * ((n + 1) ** 2)



assert cube_Sum(2) == 72
assert cube_Sum(3) == 288
assert cube_Sum(4) == 800

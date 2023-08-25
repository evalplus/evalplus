"""
Write a python function takes in an integer n and returns the sum of squares of first n even natural numbers.
"""

def square_Sum(n):  
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    return 2 * n * (n + 1) * (2 * n + 1) /3



assert square_Sum(2) == 20
assert square_Sum(3) == 56
assert square_Sum(4) == 120

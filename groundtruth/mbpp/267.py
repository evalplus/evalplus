"""
Write a python function that takes in an integer n and returns the sum of the squares of the first n odd natural numbers.
"""

def square_Sum(n):  
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n > 0, "invalid inputs" # $_CONTRACT_$
    return n * (4 * n * n - 1) / 3



assert square_Sum(2) == 10
assert square_Sum(3) == 35
assert square_Sum(4) == 84

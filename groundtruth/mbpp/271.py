"""
Write a python function that takes in an integer n and finds the sum of the first n even natural numbers that are raised to the fifth power.
"""

def even_Power_Sum(n): 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n > 0, "invalid inputs" # $_CONTRACT_$
    return sum(x ** 5 for x in range(2, 2 * n + 1, 2))



assert even_Power_Sum(2) == 1056
assert even_Power_Sum(3) == 8832
assert even_Power_Sum(1) == 32

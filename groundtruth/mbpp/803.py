"""
Write a function to check whether the given number is a perfect square or not. https://www.geeksforgeeks.org/check-if-given-number-is-perfect-square-in-cpp/
"""

def is_perfect_square(n) :
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    if n < 0:
        return False
    return n**(1/2) == int(n**(1/2))




assert not is_perfect_square(10)
assert is_perfect_square(36)
assert not is_perfect_square(14)
assert is_perfect_square(14*14)
assert not is_perfect_square(125)
assert is_perfect_square(125*125)

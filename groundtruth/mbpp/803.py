"""
Write a function to check whether the given number is a perfect square or not. https://www.geeksforgeeks.org/check-if-given-number-is-perfect-square-in-cpp/
"""

def is_perfect_square(n) :
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    i = 1
    while (i * i<= n):
        if ((n % i == 0) and (n / i == i)):
            return True     
        i = i + 1
    return False



assert not is_perfect_square(10)
assert is_perfect_square(36)
assert not is_perfect_square(14)
assert is_perfect_square(14*14)
assert not is_perfect_square(125)
assert is_perfect_square(125*125)

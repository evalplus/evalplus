
def special_factorial(n):
    """The Brazilian factorial is defined as:
    brazilian_factorial(n) = n! * (n-1)! * (n-2)! * ... * 1!
    where n > 0

    For example:
    >>> special_factorial(4)
    288

    The function will receive an integer as input and should return the special
    factorial of this integer.
    """
    assert type(n) == int, "invalid inputs" # $_CONTRACT_$
    assert n > 0, "invalid inputs" # $_CONTRACT_$

    fac, ans = 1, 1
    for i in range(2, n + 1):
        fac *= i
        ans *= fac
    return ans

def check(candidate):

    # Check some simple cases
    assert candidate(4) == 288, "Test 4"
    assert candidate(5) == 34560, "Test 5"
    assert candidate(7) == 125411328000, "Test 7"

    # Check some edge cases that are easy to work out by hand.
    assert candidate(1) == 1, "Test 1"


check(special_factorial)
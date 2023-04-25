

def largest_divisor(n: int) -> int:
    """ For a given number n, find the largest number that divides n evenly, smaller than n
    >>> largest_divisor(15)
    5
    """
    assert type(n) == int, "invalid inputs" # $_CONTRACT_$
    assert n > 1, "invalid inputs" # $_CONTRACT_$

    for i in range(2, n):
        if n % i == 0: return n // i
    return 1


METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate(3) == 1
    assert candidate(7) == 1
    assert candidate(10) == 5
    assert candidate(100) == 50
    assert candidate(49) == 7

check(largest_divisor)
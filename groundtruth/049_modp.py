

def modp(n: int, p: int):
    """Return 2^n modulo p (be aware of numerics).
    >>> modp(3, 5)
    3
    >>> modp(1101, 101)
    2
    >>> modp(0, 101)
    1
    >>> modp(3, 11)
    8
    >>> modp(100, 101)
    1
    """

    assert n >= 0 and p >= 1, "invalid inputs" # $_CONTRACT_$
    ret = 1
    for i in range(n):
        ret = (2 * ret) % p
    return ret




METADATA = {}


def check(candidate):
    assert candidate(3, 5) == 3
    assert candidate(1101, 101) == 2
    assert candidate(0, 101) == 1
    assert candidate(3, 11) == 8
    assert candidate(100, 101) == 1
    assert candidate(30, 5) == 4
    assert candidate(31, 5) == 3


check(modp)
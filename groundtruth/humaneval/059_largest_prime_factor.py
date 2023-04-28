

def largest_prime_factor(n: int):
    """Return the largest prime factor of n. Assume n > 1 and is not a prime.
    >>> largest_prime_factor(13195)
    29
    >>> largest_prime_factor(2048)
    2
    """
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    def is_prime(a): # $_CONTRACT_$
        return not (a < 2 or any(a % x == 0 for x in range(2, int(a ** 0.5) + 1))) # $_CONTRACT_$
    assert n > 1 and not is_prime(n), "invalid inputs" # $_CONTRACT_$

    isprime = [True] * (n + 1)
    for i in range(2, n + 1):
        if isprime[i]:
            for j in range(i + i, n, i):
                isprime[j] = False
    for i in range(n - 1, 0, -1):
        if isprime[i] and n % i == 0:
            return i


METADATA = {}


def check(candidate):
    assert candidate(15) == 5
    assert candidate(27) == 3
    assert candidate(63) == 7
    assert candidate(330) == 11
    assert candidate(13195) == 29


check(largest_prime_factor)
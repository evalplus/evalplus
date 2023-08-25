"""
Write a python function that takes in a non-negative number and returns the number of prime numbers less than the given non-negative number.
"""

def count_Primes_nums(n):
    assert isinstance(n, int) and n >= 0, "invalid inputs" # $_CONTRACT_$  
    return sum(all(i % j != 0 for j in range(2, i)) for i in range(2, n))



assert count_Primes_nums(5) == 2
assert count_Primes_nums(10) == 4
assert count_Primes_nums(100) == 25

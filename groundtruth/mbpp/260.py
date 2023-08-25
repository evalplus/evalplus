"""
Write a function to find the nth newman–shanks–williams prime number.
"""

def newman_prime(n): 
	assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
	assert n >= 0, "invalid inputs" # $_CONTRACT_$
	if n == 0 or n == 1: 
		return 1
	a = 1
	b = 1
	c = 1
	for _ in range(2, n + 1):
		c = 2 * b + a
		a = b
		b = c
	return c




assert newman_prime(3) == 7
assert newman_prime(4) == 17
assert newman_prime(5) == 41

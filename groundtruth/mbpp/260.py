"""
Write a function to find the nth newman–shanks–williams prime number.
"""

def newman_prime(n): 
	if n == 0 or n == 1: 
		return 1
	return 2 * newman_prime(n - 1) + newman_prime(n - 2)



assert newman_prime(3) == 7
assert newman_prime(4) == 17
assert newman_prime(5) == 41

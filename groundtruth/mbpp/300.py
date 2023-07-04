"""
Write a function to find the count of all binary sequences of length 2n such that sum of first n bits is same as sum of last n bits.
"""

def count_binary_seq(n): 
	assert isinstance(n, int) and n > 0, "invalid inputs" # $_CONTRACT_$
	nCr = 1
	res = 1
	for r in range(1, n + 1): 
		nCr = (nCr * (n + 1 - r)) / r 
		res += nCr * nCr 
	return res 

import math

assert math.isclose(count_binary_seq(1), 2.0, rel_tol=0.001)
assert math.isclose(count_binary_seq(2), 6.0, rel_tol=0.001)
assert math.isclose(count_binary_seq(3), 20.0, rel_tol=0.001)

"""
Write a function to find nth polite number. geeksforgeeks.org/n-th-polite-number/
"""

import math 
def is_polite(n): 
	assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
	assert n >= 0, "invalid inputs" # $_CONTRACT_$
	n = n + 1
	return (int)(n+(math.log((n + math.log(n, 2)), 2))) 



assert is_polite(7) == 11
assert is_polite(4) == 7
assert is_polite(9) == 13

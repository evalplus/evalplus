"""
Write a function to find the n'th lucas number.
"""

def find_lucas(n): 
	assert isinstance(n, int) and n >= 0, "invalid inputs" # $_CONTRACT_$
	if (n == 0): 
		return 2
	if (n == 1): 
		return 1
	return find_lucas(n - 1) + find_lucas(n - 2) 



assert find_lucas(9) == 76
assert find_lucas(4) == 7
assert find_lucas(3) == 4

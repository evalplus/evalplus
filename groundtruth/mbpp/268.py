"""
Write a function to find the n'th star number.
"""

def find_star_num(n): 
	assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
	assert n > 0, "invalid inputs" # $_CONTRACT_$
	return 6 * n * (n - 1) + 1 



assert find_star_num(3) == 37
assert find_star_num(4) == 73
assert find_star_num(5) == 121

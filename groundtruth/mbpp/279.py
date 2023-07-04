"""
Write a function to find the nth decagonal number.
"""

def is_num_decagonal(n): 
	assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
	assert n > 0, "invalid inputs" # $_CONTRACT_$
	return 4 * n * n - 3 * n 



assert is_num_decagonal(3) == 27
assert is_num_decagonal(7) == 175
assert is_num_decagonal(10) == 370

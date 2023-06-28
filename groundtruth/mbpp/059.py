"""
Write a function to find the nth octagonal number.
"""

def is_octagonal(n): 
	return 3 * n * n - 2 * n 



assert is_octagonal(5) == 65
assert is_octagonal(10) == 280
assert is_octagonal(15) == 645

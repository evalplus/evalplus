"""
Write a function to find the nth nonagonal number.
"""

def is_nonagonal(n): 
	return int(n * (7 * n - 5) / 2) 



assert is_nonagonal(10) == 325
assert is_nonagonal(15) == 750
assert is_nonagonal(18) == 1089

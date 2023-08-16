"""
Write a function to calculate the value of 'a' to the power 'b'.
"""

def power(a, b):
	assert isinstance(a, (int, float)), "invalid inputs" # $_CONTRACT_$
	assert isinstance(b, int), "invalid inputs" # $_CONTRACT_$
	return a ** b



assert power(3,4) == 81
assert power(2,3) == 8
assert power(5,5) == 3125

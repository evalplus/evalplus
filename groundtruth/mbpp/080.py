"""
Write a function to find the nth tetrahedral number.
"""

def tetrahedral_number(n): 
	assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
	assert n >= 0, "invalid inputs" # $_CONTRACT_$
	return (n * (n + 1) * (n + 2)) / 6



assert tetrahedral_number(5) == 35
assert tetrahedral_number(6) == 56
assert tetrahedral_number(7) == 84

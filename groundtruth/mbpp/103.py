"""
Write a function to find the Eulerian number a(n, m).
"""

def eulerian_num(n, m): 
	assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
	assert isinstance(m, int), "invalid inputs" # $_CONTRACT_$
	assert n >= 0, "invalid inputs" # $_CONTRACT_$
	assert m >= 0, "invalid inputs" # $_CONTRACT_$
	if (m >= n or n == 0): 
		return 0 
	if (m == 0): 
		return 1 
	return (n - m) * eulerian_num(n - 1, m - 1) + (m + 1) * eulerian_num(n - 1, m)



assert eulerian_num(3, 1) == 4
assert eulerian_num(4, 1) == 11
assert eulerian_num(5, 3) == 26

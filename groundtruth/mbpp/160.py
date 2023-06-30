"""
Write a function that returns integers x and y that satisfy ax + by = n as a tuple, or return None if no solution exists.
"""

def find_solution(a, b, n):
	assert isinstance(a, int), "invalid inputs" # $_CONTRACT_$
	assert isinstance(b, int), "invalid inputs" # $_CONTRACT_$
	assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
	i = 0
	while i * a <= n:
		if (n - (i * a)) % b == 0: 
			return (i, (n - (i * a)) // b)
		i = i + 1
	return None



assert find_solution(2, 3, 7) == (2, 1)
assert find_solution(4, 2, 7) == None
assert find_solution(1, 13, 17) == (4, 1)

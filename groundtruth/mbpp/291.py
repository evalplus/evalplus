"""
Write a function to find out the number of ways of painting the fence such that at most 2 adjacent posts have the same color for the given fence with n posts and k colors.
"""

def count_no_of_ways(n, k): 
	assert isinstance(n, int) and n > 0, "invalid inputs" # $_CONTRACT_$
	assert isinstance(k, int) and k > 0, "invalid inputs" # $_CONTRACT_$
	mod = 1000000007
	if n == 1:
		return k
	a = k 
	b = k * k	 
	for _ in range(2, n):
		a, b = b, ((k - 1) * (a + b)) % mod
	return b



assert count_no_of_ways(2, 4) == 16
assert count_no_of_ways(3, 2) == 6
assert count_no_of_ways(4, 4) == 228

"""
Write a function to find out the number of ways of painting the fence such that at most 2 adjacent posts have the same color for the given fence with n posts and k colors.
"""

def count_no_of_ways(n, k): 
	assert isinstance(n, int) and n > 0, "invalid inputs" # $_CONTRACT_$
	assert isinstance(k, int) and k > 0, "invalid inputs" # $_CONTRACT_$
	dp = [0] * (n + 1) 
	total = k 
	mod = 1000000007
	dp[1] = k 
	dp[2] = k * k	 
	for i in range(3,n+1): 
		dp[i] = ((k - 1) * (dp[i - 1] + dp[i - 2])) % mod 
	return dp[n]



assert count_no_of_ways(2, 4) == 16
assert count_no_of_ways(3, 2) == 6
assert count_no_of_ways(4, 4) == 228

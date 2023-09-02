"""
Write a function to find the nth jacobsthal number. https://www.geeksforgeeks.org/jacobsthal-and-jacobsthal-lucas-numbers/ 0, 1, 1, 3, 5, 11, 21, 43, 85, 171, 341, 683, 1365, 2731, ...
"""

def jacobsthal_num(n): 
	assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
	assert n >= 0, "invalid inputs" # $_CONTRACT_$
	dp = [0] * (n + 1) 
	dp[0] = 0
	dp[1] = 1
	for i in range(2, n+1): 
		dp[i] = dp[i - 1] + 2 * dp[i - 2] 
	return dp[n]



assert jacobsthal_num(5) == 11
assert jacobsthal_num(2) == 1
assert jacobsthal_num(4) == 3
assert jacobsthal_num(13) == 1365

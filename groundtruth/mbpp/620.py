"""
Write a function to find the size of the largest subset of a list of numbers so that every pair is divisible.
"""

def largest_subset(a):
	assert isinstance(a, list), "invalid inputs" # $_CONTRACT_$
	assert len(a) >= 2, "invalid inputs" # $_CONTRACT_$
	assert all(isinstance(el, (int, float)) for el in a), "invalid inputs" # $_CONTRACT_$
	n = len(a)
	dp = [0 for _ in range(n)]
	dp[n - 1] = 1; 
	for i in range(n - 2, -1, -1):
		mxm = 0
		for j in range(i + 1, n):
			if a[j] % a[i] == 0 or a[i] % a[j] == 0:
				mxm = max(mxm, dp[j])
		dp[i] = 1 + mxm
	return max(dp)



assert largest_subset([ 1, 3, 6, 13, 17, 18 ]) == 4
assert largest_subset([10, 5, 3, 15, 20]) == 3
assert largest_subset([18, 1, 3, 6, 13, 17]) == 4

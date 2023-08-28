"""
Write a function to find the maximum sum of increasing subsequence from prefix until ith index and also including a given kth element which is after i, i.e., k > i .
"""

def max_sum_increasing_subseq(a, n, index, k):
	assert isinstance(a, list), "invalid inputs" # $_CONTRACT_$
	assert all(isinstance(x, (int, float)) for x in a), "invalid inputs" # $_CONTRACT_$
	assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
	assert n == len(a), "invalid inputs" # $_CONTRACT_$
	assert isinstance(index, int), "invalid inputs" # $_CONTRACT_$
	assert 0 <= index < n, "invalid inputs" # $_CONTRACT_$
	assert isinstance(k, int), "invalid inputs" # $_CONTRACT_$
	assert index < k < n, "invalid inputs" # $_CONTRACT_$
	dp = [[0 for _ in range(n)] for _ in range(n)]
	for i in range(n):
		if a[i] > a[0]:
			dp[0][i] = a[i] + a[0]
		else:
			dp[0][i] = a[i]
	for i in range(1, n):
		for j in range(n):
			if a[j] > a[i] and j > i:
				if dp[i - 1][i] + a[j] > dp[i - 1][j]:
					dp[i][j] = dp[i - 1][i] + a[j]
				else:
					dp[i][j] = dp[i - 1][j]
			else:
				dp[i][j] = dp[i - 1][j]
	return dp[index][k]



assert max_sum_increasing_subseq([1, 101, 2, 3, 100, 4, 5 ], 7, 4, 6) == 11
assert max_sum_increasing_subseq([1, 101, 2, 3, 100, 4, 5 ], 7, 2, 5) == 7
assert max_sum_increasing_subseq([11, 15, 19, 21, 26, 28, 31], 7, 2, 4) == 71

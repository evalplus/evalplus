"""
Write a function to find the length of the longest palindromic subsequence in the given string.
"""

def lps(str1): 
	assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
	n = len(str1)
	dp = [[0] * n for _ in range(n)]
	for i in range(n - 1, -1, -1):
		dp[i][i] = 1
		for j in range(i + 1, n):
			if str1[i] == str1[j]:
				dp[i][j] = dp[i + 1][j - 1] + 2
			else:
				dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
	return dp[0][n - 1]



assert lps("TENS FOR TENS") == 5
assert lps("CARDIO FOR CARDS") == 7
assert lps("PART OF THE JOURNEY IS PART") == 9

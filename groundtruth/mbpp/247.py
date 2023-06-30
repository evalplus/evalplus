"""
Write a function to find the length of the longest palindromic subsequence in the given string.
"""

def lps(str1): 
	assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
	n = len(str1) 
	L = [[0 for x in range(n)] for x in range(n)] 
	for i in range(n): 
		L[i][i] = 1
	for cl in range(2, n+1): 
		for i in range(n-cl+1): 
			j = i+cl-1
			if str1[i] == str1[j] and cl == 2: 
				L[i][j] = 2
			elif str1[i] == str1[j]: 
				L[i][j] = L[i+1][j-1] + 2
			else: 
				L[i][j] = max(L[i][j-1], L[i+1][j]); 
	return L[0][n-1]



assert lps("TENS FOR TENS") == 5
assert lps("CARDIO FOR CARDS") == 7
assert lps("PART OF THE JOURNEY IS PART") == 9

"""
Write a function that takes in positive integers m and n and finds the number of possible sequences of length n, such that each element is a positive integer and is greater than or equal to twice the previous element but less than or equal to m.
"""

def get_total_number_of_sequences(m, n):
	assert isinstance(m, int) and m > 0, "invalid inputs" # $_CONTRACT_$ 
	assert isinstance(n, int) and n > 0, "invalid inputs" # $_CONTRACT_$
	T=[[0 for i in range(n+1)] for i in range(m+1)] 
	for i in range(m+1): 
		for j in range(n+1): 
			if i==0 or j==0: 
				T[i][j]=0
			elif i<j: 
				T[i][j]=0
			elif j==1: 
				T[i][j]=i 
			else: 
				T[i][j]=T[i-1][j]+T[i//2][j-1] 
	return T[m][n]



assert get_total_number_of_sequences(10, 4) == 4
assert get_total_number_of_sequences(5, 2) == 6
assert get_total_number_of_sequences(16, 3) == 84

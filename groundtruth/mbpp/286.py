"""
Write a function to find the largest sum of a contiguous array in the modified array which is formed by repeating the given array k times.
"""

def max_sub_array_sum_repeated(a, n, k): 
	assert isinstance(a, list), "invalid inputs" # $_CONTRACT_$
	assert len(a) > 0, "invalid inputs" # $_CONTRACT_$
	assert all(isinstance(item, (int, float)) for item in a), "invalid inputs" # $_CONTRACT_$
	assert isinstance(n, int) and n == len(a), "invalid inputs" # $_CONTRACT_$
	assert isinstance(k, int) and k >= 0, "invalid inputs" # $_CONTRACT_$
	modifed = a * k
	pre = 0	# dp[i-1]
	res = modifed[0]
	for n in modifed:
		pre = max(pre + n, n)
		res = max(pre, res)
	return res



assert max_sub_array_sum_repeated([10, 20, -30, -1], 4, 3) == 30
assert max_sub_array_sum_repeated([-1, 10, 20], 3, 2) == 59
assert max_sub_array_sum_repeated([-1, -2, -3], 3, 3) == -1

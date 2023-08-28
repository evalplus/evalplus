"""
Write a function to find the maximum sum possible by using the given equation f(n) = max( (f(n/2) + f(n/3) + f(n/4) + f(n/5)), n).
"""

def get_max_sum (n):
	assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
	assert n >= 0, "invalid inputs" # $_CONTRACT_$
	# if n = 0, f(0) = max(5(f(0), 0)), so f(0) = 5f(0) or f(0) = 0, for both cases f(0) = 0
	res = [0]
	for i in range(1, n + 1):
		res.append(max(res[i // 2] + res[i // 3] + res[i // 4] + res[i // 5], i))
	return res[n]



assert get_max_sum(60) == 106
assert get_max_sum(10) == 12
assert get_max_sum(2) == 2

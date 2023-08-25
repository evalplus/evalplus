"""
Write a function that takes in a sorted array, its length (n), and an element and returns whether the element is the majority element in the given sorted array. (The majority element is the element that occurs more than n/2 times.)
"""

from bisect import bisect_left, bisect_right
def is_majority(arr, n, x):
	assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
	assert all(isinstance(item, (int, float)) for item in arr), "invalid inputs" # $_CONTRACT_$
	assert all(a <= b for a, b in zip(arr[:n], arr[1:n])), "invalid inputs" # $_CONTRACT_$
	assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
	assert isinstance(x, (int, float)), "invalid inputs" # $_CONTRACT_$
	assert len(arr) <= n, "invalid inputs" # $_CONTRACT_$
	if x not in arr:
		return False
	l = bisect_left(arr, x)
	r = bisect_right(arr, x)
	return r - l > n / 2

assert is_majority([1, 2, 3, 3, 3, 3, 10], 7, 3) == True
assert is_majority([1, 1, 2, 4, 4, 4, 6, 6], 8, 4) == False
assert is_majority([1, 1, 1, 2, 2], 5, 1) == True

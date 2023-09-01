"""
Write a function to find kth element from the given two sorted arrays.
"""

def find_kth(arr1, arr2, k):
	assert isinstance(arr1, list), "invalid inputs" # $_CONTRACT_$
	assert isinstance(arr2, list), "invalid inputs" # $_CONTRACT_$
	assert isinstance(k, int), "invalid inputs" # $_CONTRACT_$
	assert 0 < k <= len(arr1) + len(arr2), "invalid inputs" # $_CONTRACT_$j
	return sorted(arr1 + arr2)[k - 1]



assert find_kth([2, 3, 6, 7, 9], [1, 4, 8, 10], 5) == 6
assert find_kth([100, 112, 256, 349, 770], [72, 86, 113, 119, 265, 445, 892], 7) == 256
assert find_kth([3, 4, 7, 8, 10], [2, 5, 9, 11], 6) == 8

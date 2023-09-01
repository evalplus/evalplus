"""
Write a function to find the maximum product subarray of the given array.
"""

def max_subarray_product(arr):
	assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
	assert len(arr) > 0, "invalid inputs" # $_CONTRACT_$
	assert all(isinstance(x, (int, float)) for x in arr), "invalid inputs" # $_CONTRACT_$
	max_so_far = min_ending = max_ending = arr[0]
	for n in arr[1:]:
		min_ending, max_ending = min(n, min_ending * n, max_ending * n), max(n, min_ending * n, max_ending * n)
		max_so_far = max(max_so_far, max_ending)
	return max_so_far




assert max_subarray_product([1, -2, -3, 0, 7, -8, -2]) == 112
assert max_subarray_product([6, -3, -10, 0, 2]) == 180
assert max_subarray_product([-2, -40, 0, -2, -3]) == 80

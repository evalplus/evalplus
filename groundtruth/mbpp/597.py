"""
Write a function to find kth element from the given two sorted arrays.
"""

def find_kth(arr1, arr2, k):
	assert isinstance(arr1, list), "invalid inputs" # $_CONTRACT_$
	assert isinstance(arr2, list), "invalid inputs" # $_CONTRACT_$
	assert isinstance(k, int), "invalid inputs" # $_CONTRACT_$
	assert k > 0, "invalid inputs" # $_CONTRACT_$
	assert k <= len(arr1) + len(arr2), "invalid inputs" # $_CONTRACT_$j
	m = len(arr1)
	n = len(arr2)
	sorted1 = [0] * (m + n)
	i = 0
	j = 0
	d = 0
	while (i < m and j < n):
		if (arr1[i] < arr2[j]):
			sorted1[d] = arr1[i]
			i += 1
		else:
			sorted1[d] = arr2[j]
			j += 1
		d += 1
	while (i < m):
		sorted1[d] = arr1[i]
		d += 1
		i += 1
	while (j < n):
		sorted1[d] = arr2[j]
		d += 1
		j += 1
	return sorted1[k - 1]



assert find_kth([2, 3, 6, 7, 9], [1, 4, 8, 10], 5) == 6
assert find_kth([100, 112, 256, 349, 770], [72, 86, 113, 119, 265, 445, 892], 7) == 256
assert find_kth([3, 4, 7, 8, 10], [2, 5, 9, 11], 6) == 8

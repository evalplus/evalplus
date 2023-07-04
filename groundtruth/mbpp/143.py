"""
Write a function to find number of lists present in the given tuple.
"""

def find_lists(inputs):
	assert isinstance(inputs, tuple), "invalid inputs" # $_CONTRACT_$
	return sum(isinstance(x, list) for x in inputs)


assert find_lists(([1, 2, 3, 4], [5, 6, 7, 8])) == 2
assert find_lists(([1, 2], [3, 4], [5, 6]))  == 3
assert find_lists(([9, 8, 7, 6, 5, 4, 3, 2, 1], )) == 1

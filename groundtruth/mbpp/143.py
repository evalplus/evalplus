"""
Write a function to find number of lists present in the given tuple.
"""

def find_lists(Input): 
	if isinstance(Input, list): 
		return 1
	else: 
		return len(Input) 



assert find_lists(([1, 2, 3, 4], [5, 6, 7, 8])) == 2
assert find_lists(([1, 2], [3, 4], [5, 6]))  == 3
assert find_lists(([9, 8, 7, 6, 5, 4, 3, 2, 1])) == 1

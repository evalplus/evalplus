"""
Write a function to flatten a given nested list structure.
"""

def flatten_list(list1):
	def list_check(l): # $_CONTRACT_$
		if not isinstance(l, list): # $_CONTRACT_$
			return isinstance(l, (int, float)) # $_CONTRACT_$
		else: # $_CONTRACT_$
			return all(list_check(item) for item in l) # $_CONTRACT_$
	assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
	assert list_check(list1), "invalid inputs" # $_CONTRACT_$
	result = []
	for item in list1:
		if isinstance(item, list):
			result.extend(flatten_list(item))
		else:
			result.append(item)
	return result



assert flatten_list([0, 10, [20, 30], 40, 50, [60, 70, 80], [90, 100, 110, 120]])==[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
assert flatten_list([[10, 20], [40], [30, 56, 25], [10, 20], [33], [40]])==[10, 20, 40, 30, 56, 25, 10, 20, 33, 40]
assert flatten_list([[1,2,3], [4,5,6], [10,11,12], [7,8,9]])==[1, 2, 3, 4, 5, 6, 10, 11, 12, 7, 8, 9]

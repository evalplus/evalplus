"""
Write a function to flatten a list and sum all of its elements.
"""

def recursive_list_sum(data_list):
	def list_check(l): # $_CONTRACT_$
		if not isinstance(l, list): # $_CONTRACT_$
			return isinstance(l, (int, float)) # $_CONTRACT_$
		else: # $_CONTRACT_$
			return all(list_check(item) for item in l) # $_CONTRACT_$
	assert isinstance(data_list, list), "invalid inputs" # $_CONTRACT_$
	assert list_check(data_list), "invalid inputs" # $_CONTRACT_$
	total = 0
	for element in data_list:
		if type(element) == type([]):
			total = total + recursive_list_sum(element)
		else:
			total = total + element
	return total



assert recursive_list_sum(([1, 2, [3,4],[5,6]]))==21
assert recursive_list_sum(([7, 10, [15,14],[19,41]]))==106
assert recursive_list_sum(([10, 20, [30,40],[50,60]]))==210

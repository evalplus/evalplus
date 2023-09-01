"""
Write a function to remove uneven elements in the nested mixed tuple.
"""

def even_ele(test_tuple, ): 
	res = tuple() 
	for ele in test_tuple: 
		if isinstance(ele, tuple): 
			res += (even_ele(ele), ) 
		elif ele % 2 == 0: 
			res += (ele, ) 
	return res 

def extract_even(test_tuple):
	def tuple_check(t): # $_CONTRACT_$
		if not isinstance(t, tuple): # $_CONTRACT_$
			return isinstance(t, (int, float)) # $_CONTRACT_$
		else: # $_CONTRACT_$
			return all(tuple_check(item) for item in t) # $_CONTRACT_$
	assert isinstance(test_tuple, tuple) # $_CONTRACT_$
	assert tuple_check(test_tuple) # $_CONTRACT_$
	return even_ele(test_tuple)



assert extract_even((4, 5, (7, 6, (2, 4)), 6, 8)) == (4, (6, (2, 4)), 6, 8)
assert extract_even((5, 6, (8, 7, (4, 8)), 7, 9)) == (6, (8, (4, 8)))
assert extract_even((5, 6, (9, 8, (4, 6)), 8, 10)) == (6, (8, (4, 6)), 8, 10)

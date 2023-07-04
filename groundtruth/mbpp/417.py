"""
Write a function to find common first element in given list of tuple.
"""

def group_tuples(Input): 
	assert isinstance(Input, list), "invalid inputs" # $_CONTRACT_$
	assert all(isinstance(x, tuple) for x in Input), "invalid inputs" # $_CONTRACT_$
	out = {} 
	for elem in Input: 
		try: 
			out[elem[0]].extend(elem[1:]) 
		except KeyError: 
			out[elem[0]] = list(elem) 
	return [tuple(values) for values in out.values()] 



assert group_tuples([('x', 'y'), ('x', 'z'), ('w', 't')]) == [('x', 'y', 'z'), ('w', 't')]
assert group_tuples([('a', 'b'), ('a', 'c'), ('d', 'e')]) == [('a', 'b', 'c'), ('d', 'e')]
assert group_tuples([('f', 'g'), ('f', 'g'), ('h', 'i')]) == [('f', 'g', 'g'), ('h', 'i')]

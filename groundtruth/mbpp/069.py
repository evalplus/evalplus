"""
Write a function to check whether a list contains the given sublist or not.
"""

def is_sublist(l, s):
	assert isinstance(l, list), "invalid inputs" # $_CONTRACT_$
	assert isinstance(s, list), "invalid inputs" # $_CONTRACT_$
	if len(l) < len(s):
		return False
	return any(l[i:i+len(s)] == s for i in range(len(l)-len(s)+1))



assert is_sublist([2,4,3,5,7],[3,7])==False
assert is_sublist([2,4,3,5,7],[4,3])==True
assert is_sublist([2,4,3,5,7],[1,6])==False

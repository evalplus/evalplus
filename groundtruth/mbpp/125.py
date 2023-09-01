"""
Write a function to find the maximum difference between the number of 0s 
and number of 1s in any sub-string of the given binary string.
"""

def find_length(string): 
	assert isinstance(string, str), "invalid inputs" # $_CONTRACT_$
	assert all([c in '01' for c in string]), "invalid inputs" # $_CONTRACT_$
	current_sum = 0
	max_sum = 0
	for c in string: 
		current_sum += 1 if c == '0' else -1
		if current_sum < 0: 
			current_sum = 0
		max_sum = max(current_sum, max_sum) 
	return max_sum



assert find_length("11000010001") == 6
assert find_length("10111") == 1
assert find_length("11011101100101") == 2

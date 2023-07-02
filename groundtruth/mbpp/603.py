"""
Write a function to get all lucid numbers smaller than or equal to a given integer.
"""

def get_ludic(n):
	assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
	assert n > 0, "invalid inputs" # $_CONTRACT_$
	ludics = []
	for i in range(1, n + 1):
		ludics.append(i)
	index = 1
	while(index != len(ludics)):
		first_ludic = ludics[index]
		remove_index = index + first_ludic
		while(remove_index < len(ludics)):
			ludics.remove(ludics[remove_index])
			remove_index = remove_index + first_ludic - 1
		index += 1
	return ludics



assert get_ludic(10) == [1, 2, 3, 5, 7]
assert get_ludic(25) == [1, 2, 3, 5, 7, 11, 13, 17, 23, 25]
assert get_ludic(45) == [1, 2, 3, 5, 7, 11, 13, 17, 23, 25, 29, 37, 41, 43]

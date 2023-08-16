"""
Write a function to check if the given number is woodball or not.
"""

def is_woodall(x): 
	assert isinstance(x, (int, float)), "invalid inputs" # $_CONTRACT_$
	if not isinstance(x, int):
		return False
	if x <= 0 or x % 2 == 0:
		return False
	if (x == 1): 
		return True
	x += 1 
	i = 0
	while (x % 2 == 0): 
		x /= 2
		i += 1
		if (i == x): 
			return True
	return False



assert is_woodall(383) == True
assert is_woodall(254) == False
assert is_woodall(200) == False

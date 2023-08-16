"""
Write a function to check whether the given number is undulating or not.
"""

def is_undulating(n): 
	assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
	assert n >= 0, "invalid inputs" # $_CONTRACT_$
	digits = [int(digit) for digit in str(n)]
	if len(set(digits)) != 2:
		return False
	return all(a != b for a, b in zip(digits, digits[1:]))



assert is_undulating(1212121) == True
assert is_undulating(1991) == False
assert is_undulating(121) == True

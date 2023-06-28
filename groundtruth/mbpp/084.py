"""
Write a function to find the nth number in the newman conway sequence.
"""

def sequence(n): 
	if n == 1 or n == 2: 
		return 1
	else: 
		return sequence(sequence(n-1)) + sequence(n-sequence(n-1))



assert sequence(10) == 6
assert sequence(2) == 1
assert sequence(3) == 2

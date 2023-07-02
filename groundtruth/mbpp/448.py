"""
Write a function to calculate the sum of perrin numbers.
"""

def cal_sum(n): 
	assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
	a = 3
	b = 0
	c = 2
	if (n == 0): 
		return 3
	if (n == 1): 
		return 3
	if (n == 2): 
		return 5
	sum = 5
	while (n > 2): 
		d = a + b 
		sum = sum + d 
		a = b 
		b = c 
		c = d 
		n = n-1
	return sum



assert cal_sum(9) == 49
assert cal_sum(10) == 66
assert cal_sum(11) == 88

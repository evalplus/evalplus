"""
Write a function to calculate a dog's age in dog's years.
"""

def dog_age(h_age):
 if h_age < 0:
 	exit()
 elif h_age <= 2:
	 d_age = h_age * 10.5
 else:
	 d_age = 21 + (h_age - 2)*4
 return d_age



assert dog_age(12)==61
assert dog_age(15)==73
assert dog_age(24)==109

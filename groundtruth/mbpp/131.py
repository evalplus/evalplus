"""
Write a python function to reverse only the vowels of a given string (where y is not a vowel).
"""

def reverse_vowels(str1):
	assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
	vowels = ""
	for char in str1:
		if char in "aeiouAEIOU":
			vowels += char
	result_string = ""
	for char in str1:
		if char in "aeiouAEIOU":
			result_string += vowels[-1]
			vowels = vowels[:-1]
		else:
			result_string += char
	return result_string



assert reverse_vowels("Python") == "Python"
assert reverse_vowels("USA") == "ASU"
assert reverse_vowels("ab") == "ab"

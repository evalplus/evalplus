"""
Write a python function to reverse only the vowels of a given string (where y is not a vowel).
"""

def reverse_vowels(str1):
	assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
	assert len(str1) > 0, "invalid inputs" # $_CONTRACT_$
	is_vowel = lambda x: x in 'aeiouAEIOU'
	pos = [i for i, c in enumerate(str1) if is_vowel(c)]
	return ''.join(c if not is_vowel(c) else str1[pos.pop()] for c in str1)
		


assert reverse_vowels("Python") == "Python"
assert reverse_vowels("USA") == "ASU"
assert reverse_vowels("ab") == "ab"

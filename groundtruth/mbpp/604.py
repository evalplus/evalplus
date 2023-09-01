"""
Write a function to reverse words seperated by spaces in a given string.
"""

def reverse_words(s):
	assert isinstance(s, str), "invalid inputs" # $_CONTRACT_$
	return ' '.join(reversed(s.split()))



assert reverse_words("python program")==("program python")
assert reverse_words("java language")==("language java")
assert reverse_words("indian man")==("man indian")

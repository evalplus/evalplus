"""
Write a function to remove characters from the first string which are present in the second string.
"""

def remove_dirty_chars(string, second_string): 
	assert isinstance(string, str), "invalid inputs" # $_CONTRACT_$
	assert isinstance(second_string, str), "invalid inputs" # $_CONTRACT_$
	assert len(string) > 0, "invalid inputs" # $_CONTRACT_$
	assert len(second_string) > 0, "invalid inputs" # $_CONTRACT_$
	for char in second_string:
		string = string.replace(char, '')
	return string



assert remove_dirty_chars("probasscurve", "pros") == 'bacuve'
assert remove_dirty_chars("digitalindia", "talent") == 'digiidi'
assert remove_dirty_chars("exoticmiles", "toxic") == 'emles'

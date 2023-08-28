"""
Write a function to check whether the given string starts and ends with the same character or not.
"""

import re  
def check_char(string): 
	assert isinstance(string, str), "invalid inputs" # $_CONTRACT_$
	regex = r'^[a-z]$|^([a-z]).*\1$'
	return re.search(regex, string) is not None



assert check_char("abba") == True
assert check_char("a") == True
assert check_char("abcd") == False

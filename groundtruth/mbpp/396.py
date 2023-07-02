"""
Write a function to check whether the given string starts and ends with the same character or not.
"""

import re  
regex = r'^[a-z]$|^([a-z]).*\1$'
def check_char(string): 
	assert isinstance(string, str), "invalid inputs" # $_CONTRACT_$
	if(re.search(regex, string)): 
		return "Valid" 
	else: 
		return "Invalid" 



assert check_char("abba") == "Valid"
assert check_char("a") == "Valid"
assert check_char("abcd") == "Invalid"

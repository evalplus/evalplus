"""
Write a function to remove the parenthesis and what is inbetween them from a string.
"""

import re
def remove_parenthesis(string):
    assert isinstance(string, str), "invalid inputs" # $_CONTRACT_$
    return re.sub(r"\([^)]+\)", "", string)



assert remove_parenthesis("python (chrome)")=="python "
assert remove_parenthesis("string(.abc)")=="string"
assert remove_parenthesis("alpha(num)")=="alpha"

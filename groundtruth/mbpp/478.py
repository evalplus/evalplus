"""
Write a function to remove lowercase substrings from a given string.
"""

import re
def remove_lowercase(str1):
    assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
    return re.sub('[a-z]', '', str1)



assert remove_lowercase("PYTHon")==('PYTH')
assert remove_lowercase("FInD")==('FID')
assert remove_lowercase("STRinG")==('STRG')

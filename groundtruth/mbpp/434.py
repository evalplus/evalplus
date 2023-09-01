"""
Write a function that matches a string that has an a followed by one or more b's.
"""

import re
def text_match_one(text):
    assert isinstance(text, str), "invalid inputs" # $_CONTRACT_$
    patterns = 'ab+?'
    return re.search(patterns,  text) is not None




assert text_match_one("ac")==False
assert text_match_one("dc")==False
assert text_match_one("abba")==True

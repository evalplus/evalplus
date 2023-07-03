"""
Write a function that matches a string that has an 'a' followed by one or more 'b's. https://www.w3resource.com/python-exercises/re/python-re-exercise-3.php
"""

import re
def text_match_zero_one(text):
        assert isinstance(text, str), "invalid inputs" # $_CONTRACT_$
        patterns = 'ab+?'
        if re.search(patterns,  text):
                return True
        else:
                return False



assert text_match_zero_one("ac")==False
assert text_match_zero_one("dc")==False
assert text_match_zero_one("abbbba")==True
assert text_match_zero_one("dsabbbba")==True
assert text_match_zero_one("asbbbba")==False
assert text_match_zero_one("abaaa")==True

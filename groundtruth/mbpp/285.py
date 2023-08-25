"""
Write a function that checks whether a string contains the 'a' character followed by two or three 'b' characters.
"""

import re
def text_match_two_three(text):
    assert isinstance(text, str), "invalid inputs" # $_CONTRACT_$
    patterns = 'ab{2,3}'
    return re.search(patterns, text) is not None



assert text_match_two_three("ac")==(False)
assert text_match_two_three("dc")==(False)
assert text_match_two_three("abbbba")==(True)

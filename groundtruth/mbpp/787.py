"""
Write a function that matches a string that has an a followed by three 'b'.
"""

import re
def text_match_three(text):
        patterns = 'ab{3}?'
        return re.search(patterns,  text)



assert not text_match_three("ac")
assert not text_match_three("dc")
assert text_match_three("abbbba")
assert text_match_three("caacabbbba")

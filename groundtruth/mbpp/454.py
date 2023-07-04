"""
Write a function that matches a word containing 'z'.
"""

import re
def text_match_wordz(text):
        assert isinstance(text, str), "invalid inputs" # $_CONTRACT_$
        patterns = '\w*z.\w*'
        if re.search(patterns,  text):
                return True
        else:
                return False



assert text_match_wordz("pythonz.")==True
assert text_match_wordz("xyz.")==True
assert text_match_wordz("  lang  .")==False

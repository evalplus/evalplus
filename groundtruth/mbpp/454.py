"""
Write a function that matches a word containing 'z'.
"""

import re
def text_match_wordz(text):
        assert isinstance(text, str), "invalid inputs" # $_CONTRACT_$
        return 'z' in text



assert text_match_wordz("pythonz.")==True
assert text_match_wordz("xyz.")==True
assert text_match_wordz("  lang  .")==False

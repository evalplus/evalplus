"""
Write a function that matches a string that has an 'a' followed by anything, ending in 'b'.
"""

import re
def text_starta_endb(text):
        assert isinstance(text, str), "invalid inputs" # $_CONTRACT_$
        patterns = 'a.*?b$'
        return re.search(patterns,  text)



assert text_starta_endb("aabbbb")
assert not text_starta_endb("aabAbbbc")
assert not text_starta_endb("accddbbjjj")

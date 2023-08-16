"""
Write a function to that returns true if the input string contains sequences of lowercase letters joined with an underscore and false otherwise.
"""

import re
def text_lowercase_underscore(text):
        assert isinstance(text, str), "invalid inputs" # $_CONTRACT_$
        assert len(text) > 0, "invalid inputs" # $_CONTRACT_$
        return bool(re.match('^[a-z]+(_[a-z]+)*$', text))



assert text_lowercase_underscore("aab_cbbbc")==(True)
assert text_lowercase_underscore("aab_Abbbc")==(False)
assert text_lowercase_underscore("Aaab_abbbc")==(False)

"""
Write a function that checks if a strings contains 'z', except at the start and end of the word.
"""

import re
def text_match_wordz_middle(text):
	assert isinstance(text, str), "invalid inputs" # $_CONTRACT_$
	return re.search(r'\Bz\B',  text) is not None



assert text_match_wordz_middle("pythonzabc.")==True
assert text_match_wordz_middle("zxyabc.")==False
assert text_match_wordz_middle("  lang  .")==False

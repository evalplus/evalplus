"""
Write a function to find the first adverb and their positions in a given sentence.
"""

import re
def find_adverb_position(text):
    assert isinstance(text, str), "invalid inputs" # $_CONTRACT_$
    for m in re.finditer(r"\w+ly", text):
        return (m.start(), m.end(), m.group(0))



assert find_adverb_position("clearly!! we can see the sky")==(0, 7, 'clearly')
assert find_adverb_position("seriously!! there are many roses")==(0, 9, 'seriously')
assert find_adverb_position("unfortunately!! sita is going to home")==(0, 13, 'unfortunately')

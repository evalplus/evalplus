"""
Write a function to return two words from a list of words starting with letter 'p'.
"""

import re
def start_withp(words):
    assert isinstance(words, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, str) for x in words), "invalid inputs" # $_CONTRACT_$
    for w in words:
        m = re.match("(P\w+)\W(P\w+)", w)
        if m:
            return m.groups()



assert start_withp(["Python PHP", "Java JavaScript", "c c++"])==('Python', 'PHP')
assert start_withp(["Python Programming","Java Programming"])==('Python','Programming')
assert start_withp(["Pqrst Pqr","qrstuv"])==('Pqrst','Pqr')

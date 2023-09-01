"""
Write a python function to count the upper case characters in a given string.
"""

def upper_ctr(str1):
    assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
    return sum(1 for c in str1 if c.isupper())




assert upper_ctr('PYthon') == 2
assert upper_ctr('BigData') == 2
assert upper_ctr('program') == 0

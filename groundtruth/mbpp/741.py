"""
Write a python function to check whether all the characters are same or not.
"""

def all_Characters_Same(s) :
    assert isinstance(s, str), "invalid inputs" # $_CONTRACT_$
    return all(ch == s[0] for ch in s[1:])



assert all_Characters_Same("python") == False
assert all_Characters_Same("aaa") == True
assert all_Characters_Same("data") == False

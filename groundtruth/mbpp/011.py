"""
Write a python function to remove first and last occurrence of a given character from the string.
"""

def remove_Occ(s,ch): 
    assert isinstance(s, str), "invalid inputs" # $_CONTRACT_$
    assert isinstance(ch, str), "invalid inputs" # $_CONTRACT_$
    assert len(s) > 0, "invalid inputs" # $_CONTRACT_$
    assert len(ch) == 1, "invalid inputs" # $_CONTRACT_$
    s = s.replace(ch, '', 1)
    s = s[::-1].replace(ch, '', 1)[::-1]
    return s 



assert remove_Occ("hello","l") == "heo"
assert remove_Occ("abcda","a") == "bcd"
assert remove_Occ("PHP","P") == "H"

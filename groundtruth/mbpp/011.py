"""
Write a python function to remove first and last occurrence of a given character from the string.
"""

def remove_Occ(s,ch): 
    assert isinstance(s, str), "invalid inputs" # $_CONTRACT_$
    assert isinstance(ch, str), "invalid inputs" # $_CONTRACT_$
    assert len(s) > 0, "invalid inputs" # $_CONTRACT_$
    assert len(ch) == 1, "invalid inputs" # $_CONTRACT_$
    for i in range(len(s)): 
        if (s[i] == ch): 
            s = s[0 : i] + s[i + 1:] 
            break
    for i in range(len(s) - 1,-1,-1):  
        if (s[i] == ch): 
            s = s[0 : i] + s[i + 1:] 
            break
    return s 



assert remove_Occ("hello","l") == "heo"
assert remove_Occ("abcda","a") == "bcd"
assert remove_Occ("PHP","P") == "H"

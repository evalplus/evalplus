"""
Write a python function to find the character made by adding the ASCII value of all the characters of the given string modulo 26.
"""

def get_Char(strr):  
    assert isinstance(strr, str), "invalid inputs" # $_CONTRACT_$
    summ = sum([ord(i) for i in strr])
    return chr(summ % 26)



assert get_Char("abc") == "f"
assert get_Char("gfg") == "t"
assert get_Char("ab") == "c"

"""
Write a python function to find the character made by adding the ASCII value of all the characters of the given string modulo 26.
"""

def get_Char(strr):  
    assert isinstance(strr, str), "invalid inputs" # $_CONTRACT_$
    summ = 0
    for i in range(len(strr)): 
        summ += (ord(strr[i]) - ord('a') + 1)  
    if (summ % 26 == 0): 
        return ord('z') 
    else: 
        summ = summ % 26
        return chr(ord('a') + summ - 1)



assert get_Char("abc") == "f"
assert get_Char("gfg") == "t"
assert get_Char("ab") == "c"

"""
Write a python function to find the minimum number of rotations (greater than 0) required to get the same string.
"""

def find_Rotations(s): 
    assert isinstance(s, str), "invalid inputs" # $_CONTRACT_$
    assert len(s) > 0, "invalid inputs" # $_CONTRACT_$
    tmp = s + s
    n = len(s) 
    for i in range(1,n + 1): 
        substring = tmp[i: i+n] 
        if (s == substring): 
            return i 
    return n 



assert find_Rotations("aaaa") == 1
assert find_Rotations("ab") == 2
assert find_Rotations("abc") == 3

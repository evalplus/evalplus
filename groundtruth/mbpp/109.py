"""
Write a python function to find the number of numbers with an odd value when rotating a binary string the given number of times.
"""

def odd_Equivalent(s,n): 
    assert isinstance(s, str), "invalid inputs" # $_CONTRACT_$
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert all([c in '01' for c in s]), "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    count=0
    for i in range(0,n): 
        if (s[i] == '1'): 
            count = count + 1
    return count 



assert odd_Equivalent("011001",6) == 3
assert odd_Equivalent("11011",5) == 4
assert odd_Equivalent("1010",4) == 2

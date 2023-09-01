"""
Write a python function to count minimum number of swaps required to convert one binary number represented as a string to another.
"""

def min_Swaps(str1,str2) : 
    assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
    assert isinstance(str2, str), "invalid inputs" # $_CONTRACT_$
    assert all([c in '01' for c in str1]), "invalid inputs" # $_CONTRACT_$
    assert all([c in '01' for c in str2]), "invalid inputs" # $_CONTRACT_$
    assert len(str1) == len(str2), "invalid inputs" # $_CONTRACT_$
    diff_bit = sum(str1[i] != str2[i] for i in range(len(str1)))
    if diff_bit % 2 == 0 : 
        return diff_bit // 2
    else : 
        return None



assert min_Swaps("1101","1110") == 1
assert min_Swaps("111","000") == None
assert min_Swaps("111","110") == None

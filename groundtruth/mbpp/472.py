"""
Write a python function to check whether the given list contains consecutive numbers or not.
"""

def check_Consecutive(l): 
    assert isinstance(l, list), "invalid inputs" # $_CONTRACT_$
    assert len(l) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, int) for x in l), "invalid inputs" # $_CONTRACT_$
    return sorted(l) == list(range(min(l),max(l)+1)) 



assert check_Consecutive([1,2,3,4,5]) == True
assert check_Consecutive([1,2,3,5,6]) == False
assert check_Consecutive([1,2,1]) == False

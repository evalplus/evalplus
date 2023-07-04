"""
Write a python function to find the sublist having minimum length.
"""

def Find_Min(lst): 
    assert isinstance(lst, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, list) for x in lst), "invalid inputs" # $_CONTRACT_$
    return min(lst, key=len) 



assert Find_Min([[1],[1,2],[1,2,3]]) == [1]
assert Find_Min([[1,1],[1,1,1],[1,2,7,8]]) == [1,1]
assert Find_Min([['x'],['x','y'],['x','y','z']]) == ['x']

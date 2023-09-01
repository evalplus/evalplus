"""
Write a python function to find the length of the longest sublists.
"""

def Find_Max_Length(lst):  
    assert isinstance(lst, list), "invalid inputs" # $_CONTRACT_$
    assert len(lst) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, list) for x in lst), "invalid inputs" # $_CONTRACT_$
    return len(max(lst, key = len))



assert Find_Max_Length([[1],[1,4],[5,6,7,8]]) == 4
assert Find_Max_Length([[0,1],[2,2,],[3,2,1]]) == 3
assert Find_Max_Length([[7],[22,23],[13,14,15],[10,20,30,40,50]]) == 5

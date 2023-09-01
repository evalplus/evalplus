"""
Write a python function to get the first element of each sublist.
"""

def Extract(lst): 
    assert isinstance(lst, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(l, list) for l in lst), "invalid inputs" # $_CONTRACT_$
    assert all(len(l) > 0 for l in lst), "invalid inputs" # $_CONTRACT_$
    return [item[0] for item in lst] 



assert Extract([[1, 2], [3, 4, 5], [6, 7, 8, 9]]) == [1, 3, 6]
assert Extract([[1,2,3],[4, 5]]) == [1,4]
assert Extract([[9,8,1],[1,2]]) == [9,1]

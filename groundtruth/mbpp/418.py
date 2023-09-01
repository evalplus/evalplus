"""
Write a python function to find the element of a list having maximum length.
"""

def Find_Max(lst): 
    assert isinstance(lst, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(i, list) for i in lst), "invalid inputs" # $_CONTRACT_$
    return max(lst, key = len)



assert Find_Max([['A'],['A','B'],['A','B','C']]) == ['A','B','C']
assert Find_Max([[1],[1,2],[1,2,3]]) == [1,2,3]
assert Find_Max([[1,1],[1,2,3],[1,5,6,1]]) == [1,5,6,1]

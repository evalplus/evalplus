"""
Write a python function to find the element of a list having maximum length.
"""

def Find_Max(lst): 
    maxList = max((x) for x in lst) 
    return maxList



assert Find_Max([['A'],['A','B'],['A','B','C']]) == ['A','B','C']
assert Find_Max([[1],[1,2],[1,2,3]]) == [1,2,3]
assert Find_Max([[1,1],[1,2,3],[1,5,6,1]]) == [1,5,6,1]

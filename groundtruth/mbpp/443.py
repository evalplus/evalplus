"""
Write a python function to find the largest negative number from the given list.
"""

def largest_neg(list1): 
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(i, (int, float)) for i in list1), "invalid inputs" # $_CONTRACT_$
    max = list1[0] 
    for x in list1: 
        if x < max : 
             max = x  
    return max



assert largest_neg([1,2,3,-4,-6]) == -6
assert largest_neg([1,2,3,-8,-9]) == -9
assert largest_neg([1,2,3,4,-1]) == -1

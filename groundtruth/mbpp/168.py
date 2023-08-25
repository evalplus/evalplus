"""
Write a function to count the number of occurrences of a number in a given list.
"""

def frequency(a,x): 
    assert isinstance(a, list), "invalid inputs" # $_CONTRACT_$
    assert isinstance(x, (int, float)), "invalid inputs" # $_CONTRACT_$
    return a.count(x)



assert frequency([1,2,3], 4) == 0
assert frequency([1,2,2,3,3,3,4], 3) == 3
assert frequency([0,1,2,3,1,2], 1) == 2

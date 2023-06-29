"""
Write a python function to count true booleans in the given list.
"""

def count(lst):   
    assert isinstance(lst, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, bool) for x in lst), "invalid inputs" # $_CONTRACT_$
    return sum(lst) 



assert count([True,False,True]) == 2
assert count([False,False]) == 0
assert count([True,True,True]) == 3

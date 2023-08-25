"""
Write a python function to check if the elements of a given list are unique or not.
"""

def all_unique(test_list):
    assert isinstance(test_list, list), "invalid inputs" # $_CONTRACT_$
    return len(test_list) == len(set(test_list))



assert all_unique([1,2,3]) == True
assert all_unique([1,2,1,2]) == False
assert all_unique([1,2,3,4,5]) == True

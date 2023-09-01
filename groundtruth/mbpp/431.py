"""
Write a function that takes two lists and returns true if they have at least one common element.
"""

def common_element(list1, list2):
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    assert isinstance(list2, list), "invalid inputs" # $_CONTRACT_$
    return any(item in list2 for item in list1)


assert common_element([1,2,3,4,5], [5,6,7,8,9])==True
assert common_element([1,2,3,4,5], [6,7,8,9])==False
assert common_element(['a','b','c'], ['d','b','e'])==True

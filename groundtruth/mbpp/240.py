"""
Write a function that takes in two lists and replaces the last element of the first list with the elements of the second list.
"""

def replace_list(list1, list2):
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    assert isinstance(list2, list), "invalid inputs" # $_CONTRACT_$
    list1[-1:] = list2
    replace_list=list1
    return replace_list




assert replace_list([1, 3, 5, 7, 9, 10],[2, 4, 6, 8])==[1, 3, 5, 7, 9, 2, 4, 6, 8]
assert replace_list([1,2,3,4,5],[5,6,7,8])==[1,2,3,4,5,6,7,8]
assert replace_list(["red","blue","green"],["yellow"])==["red","blue","yellow"]

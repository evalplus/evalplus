"""
Write a function to check whether a specified list is sorted or not.
"""

def issort_list(list1):
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    return all(a <= b for a, b in zip(list1, list1[1:]))



assert issort_list([1,2,4,6,8,10,12,14,16,17])==True
assert issort_list([1, 2, 4, 6, 8, 10, 12, 14, 20, 17])==False
assert issort_list([1, 2, 4, 6, 8, 10,15,14,20])==False

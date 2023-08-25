"""
Write a python function that returns the number of integer elements in a given list.
"""

def count_integer(list1):
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    return sum(isinstance(x, int) for x in list1)



assert count_integer([1,2,'abc',1.2]) == 2
assert count_integer([1,2,3]) == 3
assert count_integer([1,1.2,4,5.1]) == 2

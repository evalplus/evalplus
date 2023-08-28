"""
Write a python function to remove odd numbers from a given list.
"""

def remove_odd(l):
    assert isinstance(l, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(i, int) for i in l), "invalid inputs" # $_CONTRACT_$
    return [i for i in l if i % 2 == 0]



assert remove_odd([1,2,3]) == [2]
assert remove_odd([2,4,6]) == [2,4,6]
assert remove_odd([10,20,3]) == [10,20]

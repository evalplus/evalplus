"""
Write a python function to find the last position of an element in a sorted array.
"""

def last(arr,x):
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(i, (int, arr)) for i in arr), "invalid inputs" # $_CONTRACT_$
    assert all(a <= b for a, b in zip(arr, arr[1:])), "invalid inputs" # $_CONTRACT_$
    assert isinstance(x, (int, float)), "invalid inputs" # $_CONTRACT_$
    assert x in arr, "invalid inputs" # $_CONTRACT_$
    return len(arr)-arr[::-1].index(x) - 1


assert last([1,2,3],1) == 0
assert last([1,1,1,2,3,4],1) == 2
assert last([2,2,3,3,6,8,9],3) == 3

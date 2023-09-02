"""
Write a python function to find the sum of an array.
"""

def _sum(arr):  
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(n, (int, float)) for n in arr), "invalid inputs" # $_CONTRACT_$
    return sum(arr)



assert _sum([1, 2, 3]) == 6
assert _sum([15, 12, 13, 10]) == 50
assert _sum([0, 1, 2]) == 3

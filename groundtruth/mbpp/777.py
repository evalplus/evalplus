"""
Write a python function to find the sum of non-repeated elements in a given list.
"""

def find_sum(arr): 
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, (int, float)) for x in arr), "invalid inputs" # $_CONTRACT_$
    return sum(set(arr))



assert find_sum([1,2,3,1,1,4,5,6]) == 21
assert find_sum([1,10,9,4,2,10,10,45,4]) == 71
assert find_sum([12,10,9,45,2,10,10,45,10]) == 78

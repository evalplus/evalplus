"""
Write a python function to find sum of products of all possible sublists of a given list. https://www.geeksforgeeks.org/sum-of-products-of-all-possible-subarrays/
"""

def sum_Of_Subarray_Prod(arr):
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert len(arr) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, (int, float)) for x in arr), "invalid inputs" # $_CONTRACT_$
    result = 0  # final result
    partial = 0 # partial sum
    # stimulate the recursion
    while arr != []:
        partial = arr[-1] * (1 + partial)
        result += partial
        arr.pop()
    return result



assert sum_Of_Subarray_Prod([1,2,3]) == 20
assert sum_Of_Subarray_Prod([1,2]) == 5
assert sum_Of_Subarray_Prod([1,2,3,4]) == 84

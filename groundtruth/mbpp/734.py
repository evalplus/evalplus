"""
Write a python function to find sum of products of all possible sublists of a given list. https://www.geeksforgeeks.org/sum-of-products-of-all-possible-subarrays/
"""

def sum_Of_Subarray_Prod(arr):
    ans = 0
    res = 0
    i = len(arr) - 1
    while (i >= 0):
        incr = arr[i]*(1 + res)
        ans += incr
        res = incr
        i -= 1
    return (ans)



assert sum_Of_Subarray_Prod([1,2,3]) == 20
assert sum_Of_Subarray_Prod([1,2]) == 5
assert sum_Of_Subarray_Prod([1,2,3,4]) == 84

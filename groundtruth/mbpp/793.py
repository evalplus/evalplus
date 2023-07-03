"""
Write a python function to find the last position of an element in a sorted array.
"""

def last(arr,x):
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(i, (int, arr)) for i in arr), "invalid inputs" # $_CONTRACT_$
    assert all(a <= b for a, b in zip(arr, arr[1:])), "invalid inputs" # $_CONTRACT_$
    assert isinstance(x, (int, float)), "invalid inputs" # $_CONTRACT_$
    n = len(arr)
    low = 0
    high = n - 1
    res = -1  
    while (low <= high):
        mid = (low + high) // 2 
        if arr[mid] > x:
            high = mid - 1
        elif arr[mid] < x:
            low = mid + 1
        else:
            res = mid
            low = mid + 1
    return res



assert last([1,2,3],1) == 0
assert last([1,1,1,2,3,4],1) == 2
assert last([2,2,3,3,6,8,9],3) == 3

"""
Write a python function to find the element that appears only once in a sorted array.
"""

def search(arr):
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, int) for x in arr), "invalid inputs" # $_CONTRACT_$
    assert all(a <= b for a, b in zip(arr, arr[1:])), "invalid inputs" # $_CONTRACT_$
    n = len(arr)
    XOR = 0
    for i in range(n) :
        XOR = XOR ^ arr[i]
    return (XOR)



assert search([1,1,2,2,3]) == 3
assert search([1,1,3,3,4,4,5,5,7,7,8]) == 8
assert search([1,2,2,3,3,4,4]) == 1

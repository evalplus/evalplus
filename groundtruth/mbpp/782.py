"""
Write a python function to find the sum of all odd length subarrays. https://www.geeksforgeeks.org/sum-of-all-odd-length-subarrays/
"""

def odd_length_sum(arr):
    Sum = 0
    l = len(arr)
    for i in range(l):
        Sum += ((((i + 1) *(l - i) + 1) // 2) * arr[i])
    return Sum



assert odd_length_sum([1,2,4]) == 14
assert odd_length_sum([1,2,1,2]) == 15
assert odd_length_sum([1,7]) == 8

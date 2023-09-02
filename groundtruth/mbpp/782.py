"""
Write a python function to find the sum of all odd length subarrays. https://www.geeksforgeeks.org/sum-of-all-odd-length-subarrays/
"""

def odd_length_sum(arr):
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, (int, float)) for x in arr), "invalid inputs" # $_CONTRACT_$
    sum_ = 0
    n = len(arr)
    for i in range(n):
        # arr[i] occurs (i + 1) * (n - i) times in all subarrays
        times = ((i + 1) * (n - i) + 1) // 2
        sum_ += arr[i] * times
    return sum_



assert odd_length_sum([1,2,4]) == 14
assert odd_length_sum([1,2,1,2]) == 15
assert odd_length_sum([1,7]) == 8

"""
Write a python function to find the sum of even numbers at even positions of a list.
"""

def sum_even_and_even_index(arr):  
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, int) for x in arr), "invalid inputs" # $_CONTRACT_$
    i = 0
    sum = 0
    for i in range(0, len(arr),2): 
        if (arr[i] % 2 == 0) : 
            sum += arr[i]  
    return sum



assert sum_even_and_even_index([5, 6, 12, 1, 18, 8]) == 30
assert sum_even_and_even_index([3, 20, 17, 9, 2, 10, 18, 13, 6, 18]) == 26
assert sum_even_and_even_index([5, 6, 12, 1]) == 12

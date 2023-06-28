"""
Write a python function to find the minimum difference between any two elements in a given array. https://www.geeksforgeeks.org/find-minimum-difference-pair/
"""

def find_min_diff(arr,n): 
    arr = sorted(arr) 
    diff = 10**20 
    for i in range(n-1): 
        if arr[i+1] - arr[i] < diff: 
            diff = arr[i+1] - arr[i]  
    return diff 



assert find_min_diff((1,5,3,19,18,25),6) == 1
assert find_min_diff((4,3,2,6),4) == 1
assert find_min_diff((30,5,20,9),4) == 4

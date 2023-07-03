"""
Write a python function to count the number of rotations required to generate a sorted array. https://www.geeksforgeeks.org/count-of-rotations-required-to-generate-a-sorted-array/
"""

def count_rotation(arr):   
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, (int, float)) for x in arr), "invalid inputs" # $_CONTRACT_$
    for i in range (1,len(arr)): 
        if (arr[i] < arr[i - 1]): 
            return i  
    return 0



assert count_rotation([3,2,1]) == 1
assert count_rotation([4,5,1,2,3]) == 2
assert count_rotation([7,8,9,1,2,3]) == 3
assert count_rotation([1,2,3]) == 0
assert count_rotation([1,3,2]) == 2

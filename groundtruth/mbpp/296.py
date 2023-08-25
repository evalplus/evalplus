"""
Write a python function to count inversions in an array.
"""

def get_Inv_Count(arr): 
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert len(arr) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, (int, float)) for x in arr), "invalid inputs" # $_CONTRACT_$
    # consider use merge sort, but for simplicity, use brute force
    inv_count = 0
    for i in range(len(arr)): 
        for j in range(i + 1, len(arr)): 
            if (arr[i] > arr[j]): 
                inv_count += 1
    return inv_count 



assert get_Inv_Count([1,20,6,4,5]) == 5
assert get_Inv_Count([1,2,1]) == 1
assert get_Inv_Count([1,2,5,6,1]) == 3

"""
Write a python function to find a pair with highest product from a given array of integers.
"""

def max_Product(arr): 
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(i, int) for i in arr), "invalid inputs" # $_CONTRACT_$
    arr_len = len(arr) 
    if (arr_len < 2): 
        return ("No pairs exists")           
    x = arr[0]; y = arr[1]      
    for i in range(0,arr_len): 
        for j in range(i + 1,arr_len): 
            if (arr[i] * arr[j] > x * y): 
                x = arr[i]; y = arr[j] 
    return x,y    



assert max_Product([1,2,3,4,7,0,8,4]) == (7,8)
assert max_Product([0,-1,-2,-4,5,0,-6]) == (-4,-6)
assert max_Product([1,2,3]) == (2,3)

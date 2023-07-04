"""
Write a function to check whether the product of numbers in a list is even or not.
"""

def is_product_even(arr): 
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert len(arr) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, int) for x in arr), "invalid inputs" # $_CONTRACT_$
    for i in range(len(arr)): 
        if (arr[i] & 1) == 0: 
            return True
    return False



assert is_product_even([1,2,3])
assert is_product_even([1,2,1,4])
assert not is_product_even([1,1])

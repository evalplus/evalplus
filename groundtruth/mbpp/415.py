"""
Write a python function to find a pair with highest product from a given array of integers.
"""

def max_Product(arr): 
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert len(arr) >= 2, "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(i, int) for i in arr), "invalid inputs" # $_CONTRACT_$
    pairs = [(a, b) for a in arr for b in arr if a != b]
    return max(pairs, key=lambda x: x[0] * x[1])





assert max_Product([1,2,3,4,7,0,8,4]) == (7,8)
assert max_Product([0,-1,-2,-4,5,0,-6]) == (-4,-6)
assert max_Product([1,2,3]) == (2,3)

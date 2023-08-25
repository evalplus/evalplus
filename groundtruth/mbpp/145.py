"""
Write a python function to find the maximum difference between any two elements in a given array.
"""

def max_Abs_Diff(arr): 
    assert isinstance(arr, (tuple, list)), "invalid inputs" # $_CONTRACT_$
    assert len(arr) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, (int, float)) for x in arr), "invalid inputs" # $_CONTRACT_$
    return max(arr) - min(arr)



assert max_Abs_Diff((2,1,5,3)) == 4
assert max_Abs_Diff((9,3,2,5,1)) == 8
assert max_Abs_Diff((3,2,1)) == 2

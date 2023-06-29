"""
Write a function to find whether a given array of integers contains any duplicate element.
"""

def test_duplicate(arraynums):
    assert isinstance(arraynums, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(item, int) for item in arraynums), "invalid inputs" # $_CONTRACT_$
    nums_set = set(arraynums)    
    return len(arraynums) != len(nums_set)     



assert test_duplicate(([1,2,3,4,5]))==False
assert test_duplicate(([1,2,3,4, 4]))==True
assert test_duplicate([1,1,2,2,3,3,4,4,5])==True

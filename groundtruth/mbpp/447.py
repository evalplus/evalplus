"""
Write a function to find cubes of individual elements in a list.
"""

def cube_nums(nums):
    assert isinstance(nums, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(n, (int, float)) for n in nums), "invalid inputs" # $_CONTRACT_$
    return [n**3 for n in nums]



assert cube_nums([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])==[1, 8, 27, 64, 125, 216, 343, 512, 729, 1000]
assert cube_nums([10,20,30])==([1000, 8000, 27000])
assert cube_nums([12,15])==([1728, 3375])

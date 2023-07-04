"""
Write a function to filter odd numbers.
"""

def filter_oddnumbers(nums):
    assert isinstance(nums, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(n, int) for n in nums), "invalid inputs" # $_CONTRACT_$
    odd_nums = list(filter(lambda x: x%2 != 0, nums))
    return odd_nums



assert filter_oddnumbers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])==[1,3,5,7,9]
assert filter_oddnumbers([10,20,45,67,84,93])==[45,67,93]
assert filter_oddnumbers([5,7,9,8,6,4,3])==[5,7,9,3]

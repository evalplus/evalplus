"""
Write a function to find squares of individual elements in a list.
"""

def square_nums(nums):
 assert isinstance(nums, list), "invalid inputs" # $_CONTRACT_$
 assert all(isinstance(i, (int, float)) for i in nums), "invalid inputs" # $_CONTRACT_$
 square_nums = list(map(lambda x: x ** 2, nums))
 return square_nums



assert square_nums([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])==[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
assert square_nums([10,20,30])==([100,400,900])
assert square_nums([12,15])==([144,225])

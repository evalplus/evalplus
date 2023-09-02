"""
Write a python function to check whether every odd index contains odd numbers of a given list.
"""

def odd_position(nums):
	assert isinstance(nums, list), "invalid inputs" # $_CONTRACT_$
	assert all(isinstance(n, int) for n in nums), "invalid inputs" # $_CONTRACT_$
	return all(n % 2 == 1 for n in nums[1::2])



assert odd_position([2,1,4,3,6,7,6,3]) == True
assert odd_position([4,1,2]) == True
assert odd_position([1,2,3]) == False

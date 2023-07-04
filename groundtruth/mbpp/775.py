"""
Write a python function to check whether every odd index contains odd numbers of a given list.
"""

def odd_position(nums):
	assert isinstance(nums, list), "invalid inputs" # $_CONTRACT_$
	assert all(isinstance(i, int) for i in nums), "invalid inputs" # $_CONTRACT_$
	return all(nums[i]%2==i%2 for i in range(len(nums)))



assert odd_position([2,1,4,3,6,7,6,3]) == True
assert odd_position([4,1,2]) == True
assert odd_position([1,2,3]) == False

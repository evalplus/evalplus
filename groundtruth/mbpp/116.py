"""
Write a function to convert a given tuple of positive integers into a single integer.
"""

def tuple_to_int(nums):
    result = int(''.join(map(str,nums)))
    return result



assert tuple_to_int((1,2,3))==123
assert tuple_to_int((4,5,6))==456
assert tuple_to_int((5,6,7))==567

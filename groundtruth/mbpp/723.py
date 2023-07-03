"""
The input is defined as two lists of the same length. Write a function to count indices where the lists have the same values.
"""

from operator import eq
def count_same_pair(nums1, nums2):
    assert isinstance(nums1, list), "invalid inputs" # $_CONTRACT_$
    assert isinstance(nums2, list), "invalid inputs" # $_CONTRACT_$
    assert len(nums1) == len(nums2), "invalid inputs" # $_CONTRACT_$
    assert all(hasattr(el, '__eq__') for el in nums1), "invalid inputs" # $_CONTRACT_$
    result = sum(map(eq, nums1, nums2))
    return result



assert count_same_pair([1, 2, 3, 4, 5, 6, 7, 8],[2, 2, 3, 1, 2, 6, 7, 9])==4
assert count_same_pair([0, 1, 2, -1, -5, 6, 0, -3, -2, 3, 4, 6, 8],[2, 1, 2, -1, -5, 6, 4, -3, -2, 3, 4, 6, 8])==11
assert count_same_pair([2, 4, -6, -9, 11, -12, 14, -5, 17],[2, 1, 2, -1, -5, 6, 4, -3, -2])==1
assert count_same_pair([0, 1, 1, 2],[0, 1, 2, 2])==3

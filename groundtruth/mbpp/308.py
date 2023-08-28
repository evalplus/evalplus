"""
Write a function to find the specified number of largest products from two given lists, selecting one factor from each list.
"""

def large_product(nums1, nums2, N):
    assert isinstance(nums1, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, (int, float)) for x in nums1), "invalid inputs" # $_CONTRACT_$
    assert isinstance(nums2, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, (int, float)) for x in nums2), "invalid inputs" # $_CONTRACT_$
    assert isinstance(N, int), "invalid inputs" # $_CONTRACT_$
    assert 0 <= N <= len(nums1) * len(nums2), "invalid inputs" # $_CONTRACT_$
    result = sorted([x*y for x in nums1 for y in nums2], reverse=True)[:N]
    return result



assert large_product([1, 2, 3, 4, 5, 6],[3, 6, 8, 9, 10, 6],3)==[60, 54, 50]
assert large_product([1, 2, 3, 4, 5, 6],[3, 6, 8, 9, 10, 6],4)==[60, 54, 50, 48]
assert large_product([1, 2, 3, 4, 5, 6],[3, 6, 8, 9, 10, 6],5)==[60, 54, 50, 48, 45]

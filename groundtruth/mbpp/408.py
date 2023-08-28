"""
Write a function to find k number of smallest pairs which consist of one element from the first array and one element from the second array.
"""

import heapq
def k_smallest_pairs(nums1, nums2, k):
    assert isinstance(nums1, list), "invalid inputs" # $_CONTRACT_$
    assert isinstance(nums2, list), "invalid inputs" # $_CONTRACT_$
    assert len(nums1) > 0, "invalid inputs" # $_CONTRACT_$
    assert len(nums2) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(el, (int, float)) for el in nums1), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(el, (int, float)) for el in nums2), "invalid inputs" # $_CONTRACT_$
    assert isinstance(k, int), "invalid inputs" # $_CONTRACT_$
    assert 0 <= k <= len(nums1) * len(nums2), "invalid inputs" # $_CONTRACT_$
    nums1.sort()
    nums2.sort()
    return [(nums1[i], nums2[j]) for i in range(min(k, len(nums1))) for j in range(min(k, len(nums2)))][:k]



assert set(k_smallest_pairs([1,3,7],[2,4,6],2))==set([(1, 2), (1, 4)])
assert set(k_smallest_pairs([1,3,7],[2,4,6],1))==set([(1, 2)])
assert set(k_smallest_pairs([1,3,7],[2,4,6],7))==set([(1, 2), (1, 4), (3, 2), (1, 6), (3, 4), (3, 6), (7, 2)])

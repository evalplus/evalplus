"""
Write a function to find k number of smallest pairs which consist of one element from the first array and one element from the second array.
"""

import heapq
def k_smallest_pairs(nums1, nums2, k):
    assert isinstance(nums1, list), "invalid inputs" # $_CONTRACT_$
    assert isinstance(nums2, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(el, (int, float)) for el in nums1), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(el, (int, float)) for el in nums2), "invalid inputs" # $_CONTRACT_$
    assert isinstance(k, int), "invalid inputs" # $_CONTRACT_$
    queue = []
    def push(i, j):
        if i < len(nums1) and j < len(nums2):
            heapq.heappush(queue, [nums1[i] + nums2[j], i, j])
    push(0, 0)
    pairs = []
    while queue and len(pairs) < k:
        _, i, j = heapq.heappop(queue)
        pairs.append([nums1[i], nums2[j]])
        push(i, j + 1)
        if j == 0:
            push(i + 1, 0)
    return pairs



assert k_smallest_pairs([1,3,7],[2,4,6],2)==[[1, 2], [1, 4]]
assert k_smallest_pairs([1,3,7],[2,4,6],1)==[[1, 2]]
assert k_smallest_pairs([1,3,7],[2,4,6],7)==[[1, 2], [1, 4], [3, 2], [1, 6], [3, 4], [3, 6], [7, 2]]

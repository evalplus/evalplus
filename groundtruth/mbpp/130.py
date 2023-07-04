"""
Write a function to find the item with maximum frequency in a given list.
"""

from collections import defaultdict
def max_occurrences(nums):
    assert isinstance(nums, list), "invalid inputs" # $_CONTRACT_$
    assert len(nums) > 0, "invalid inputs" # $_CONTRACT_$
    dict = defaultdict(int)
    for i in nums:
        dict[i] += 1
    result = max(dict.items(), key=lambda x: x[1]) 
    return result[0]



assert max_occurrences([2,3,8,4,7,9,8,2,6,5,1,6,1,2,3,2,4,6,9,1,2])==2
assert max_occurrences([2,3,8,4,7,9,8,7,9,15,14,10,12,13,16,18])==8
assert max_occurrences([10,20,20,30,40,90,80,50,30,20,50,10])==20

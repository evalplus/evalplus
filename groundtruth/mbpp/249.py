"""
Write a function to find the intersection of two arrays.
"""

def intersection_array(array_nums1,array_nums2):
    assert isinstance(array_nums1, list), "invalid inputs" # $_CONTRACT_$
    assert isinstance(array_nums2, list), "invalid inputs" # $_CONTRACT_$
    return list(set(array_nums1) & set(array_nums2))



assert set(intersection_array([1, 2, 3, 5, 7, 8, 9, 10],[1, 2, 4, 8, 9])) == set([1, 2, 8, 9])
assert set(intersection_array([1, 2, 3, 5, 7, 8, 9, 10],[3,5,7,9])) == set([3,5,7,9])
assert set(intersection_array([1, 2, 3, 5, 7, 8, 9, 10],[10,20,30,40])) == set([10])

"""
Write a function to find the sum of numbers in a list within a range specified by two indices.
"""

def sum_range_list(list1, m, n):                                                                                                                                                                                                
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(item, (int, float)) for item in list1), "invalid inputs" # $_CONTRACT_$
    assert isinstance(m, int), "invalid inputs" # $_CONTRACT_$
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert 0 <= m < len(list1), "invalid inputs" # $_CONTRACT_$
    assert 0 <= n < len(list1), "invalid inputs" # $_CONTRACT_$
    return sum(list1[m : n + 1])



assert sum_range_list([2,1,5,6,8,3,4,9,10,11,8,12], 8, 10) == 29
assert sum_range_list([2,1,5,6,8,3,4,9,10,11,8,12], 5, 7) == 16
assert sum_range_list([2,1,5,6,8,3,4,9,10,11,8,12], 7, 10) == 38

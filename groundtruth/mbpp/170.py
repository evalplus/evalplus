"""
Write a function to find the sum of numbers in a list within a range specified by two indices.
"""

def sum_range_list(list1, m, n):                                                                                                                                                                                                
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    assert isinstance(m, int), "invalid inputs" # $_CONTRACT_$
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert m >= 0, "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    assert m < len(list1), "invalid inputs" # $_CONTRACT_$
    assert n < len(list1), "invalid inputs" # $_CONTRACT_$
    sum_range = 0                                                                                                                                                                                                         
    for i in range(m, n+1, 1):                                                                                                                                                                                        
        sum_range += list1[i]                                                                                                                                                                                                  
    return sum_range   



assert sum_range_list([2,1,5,6,8,3,4,9,10,11,8,12], 8, 10) == 29
assert sum_range_list([2,1,5,6,8,3,4,9,10,11,8,12], 5, 7) == 16
assert sum_range_list([2,1,5,6,8,3,4,9,10,11,8,12], 7, 10) == 38

"""
Write a python function which takes a list and returns a list with the same elements, but the k'th element removed.
"""

def remove_kth_element(list1, L):
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    assert isinstance(L, int), "invalid inputs" # $_CONTRACT_$
    assert 0 < L <= len(list1), "invalid inputs" # $_CONTRACT_$
    return  list1[:L-1] + list1[L:]



assert remove_kth_element([1,1,2,3,4,4,5,1],3)==[1, 1, 3, 4, 4, 5, 1]
assert remove_kth_element([0, 0, 1, 2, 3, 4, 4, 5, 6, 6, 6, 7, 8, 9, 4, 4],4)==[0, 0, 1, 3, 4, 4, 5, 6, 6, 6, 7, 8, 9, 4, 4]
assert remove_kth_element([10, 10, 15, 19, 18, 18, 17, 26, 26, 17, 18, 10],5)==[10,10,15,19, 18, 17, 26, 26, 17, 18, 10]

"""
Write a function that takes in a list and an integer L and splits the given list into two parts where the length of the first part of the list is L, and returns the resulting lists in a tuple.
"""

def split_two_parts(list1, L):
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    assert isinstance(L, int), "invalid inputs" # $_CONTRACT_$
    assert L <= len(list1), "invalid inputs" # $_CONTRACT_$
    return list1[:L], list1[L:]



assert split_two_parts([1,1,2,3,4,4,5,1],3)==([1, 1, 2], [3, 4, 4, 5, 1])
assert split_two_parts(['a', 'b', 'c', 'd'],2)==(['a', 'b'], ['c', 'd'])
assert split_two_parts(['p', 'y', 't', 'h', 'o', 'n'],4)==(['p', 'y', 't', 'h'], ['o', 'n'])

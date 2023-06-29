"""
Write a function to find the common elements in given nested lists.
"""

def common_in_nested_lists(nestedlist):
    assert isinstance(nestedlist, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, list) for x in nestedlist), "invalid inputs" # $_CONTRACT_$
    assert all(all(isinstance(y, int) for y in x) for x in nestedlist), "invalid inputs" # $_CONTRACT_$
    result = list(set.intersection(*map(set, nestedlist)))
    return result



assert set(common_in_nested_lists([[12, 18, 23, 25, 45], [7, 12, 18, 24, 28], [1, 5, 8, 12, 15, 16, 18]]))==set([18, 12])
assert set(common_in_nested_lists([[12, 5, 23, 25, 45], [7, 11, 5, 23, 28], [1, 5, 8, 18, 23, 16]]))==set([5,23])
assert set(common_in_nested_lists([[2, 3,4, 1], [4, 5], [6,4, 8],[4, 5], [6, 8,4]]))==set([4])

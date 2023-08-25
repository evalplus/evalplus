"""
Write a function to find the list of maximum length in a list of lists.
"""

def max_length(list1):
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, list) for x in list1), "invalid inputs" # $_CONTRACT_$
    return max([(len(x), x) for x in list1], key=lambda x: x[0])



assert max_length([[0], [1, 3], [5, 7], [9, 11], [13, 15, 17]])==(3, [13, 15, 17])
assert max_length([[1], [5, 7], [10, 12, 14,15]])==(4, [10, 12, 14,15])
assert max_length([[5], [15,20,25]])==(3, [15,20,25])

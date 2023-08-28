"""
Write a function to find the list with maximum length.
"""

def max_length_list(input_list):
    assert isinstance(input_list, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, list) for x in input_list), "invalid inputs" # $_CONTRACT_$
    if not input_list:
        return (0, [])
    return max([(len(x), x) for x in input_list], key=lambda x: x[0])



assert max_length_list([[0], [1, 3], [5, 7], [9, 11], [13, 15, 17]])==(3, [13, 15, 17])
assert max_length_list([[1,2,3,4,5],[1,2,3,4],[1,2,3],[1,2],[1]])==(5,[1,2,3,4,5])
assert max_length_list([[3,4,5],[6,7,8,9],[10,11,12]])==(4,[6,7,8,9])

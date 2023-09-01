"""
Write a function to count the number of sublists containing a particular element.
"""

def count_element_in_list(list1, x): 
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(i, list) for i in list1), "invalid inputs" # $_CONTRACT_$
    return sum(x in sublist for sublist in list1)



assert count_element_in_list([[1, 3], [5, 7], [1, 11], [1, 15, 7]],1)==3
assert count_element_in_list([['A', 'B'], ['A', 'C'], ['A', 'D', 'E'], ['B', 'C', 'D']],'A')==3
assert count_element_in_list([['A', 'B'], ['A', 'C'], ['A', 'D', 'E'], ['B', 'C', 'D']],'E')==1

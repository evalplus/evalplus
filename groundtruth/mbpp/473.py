"""
Write a function to find the tuple intersection of elements in the given tuple list irrespective of their order.
"""

def tuple_intersection(test_list1, test_list2):
  assert isinstance(test_list1, list), "invalid inputs" # $_CONTRACT_$
  assert isinstance(test_list2, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(ele, tuple) for ele in test_list1), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(ele, tuple) for ele in test_list2), "invalid inputs" # $_CONTRACT_$
  res = set([tuple(sorted(ele)) for ele in test_list1]) & set([tuple(sorted(ele)) for ele in test_list2])
  return (res)



assert tuple_intersection([(3, 4), (5, 6), (9, 10), (4, 5)] , [(5, 4), (3, 4), (6, 5), (9, 11)]) == {(4, 5), (3, 4), (5, 6)}
assert tuple_intersection([(4, 1), (7, 4), (11, 13), (17, 14)] , [(1, 4), (7, 4), (16, 12), (10, 13)]) == {(4, 7), (1, 4)}
assert tuple_intersection([(2, 1), (3, 2), (1, 3), (1, 4)] , [(11, 2), (2, 3), (6, 2), (1, 3)]) == {(1, 3), (2, 3)}

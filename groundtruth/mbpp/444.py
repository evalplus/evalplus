"""
Write a function to trim each tuple by k in the given tuple list.
"""

def trim_tuple(test_list, K):
  assert isinstance(test_list, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(ele, tuple) for ele in test_list), "invalid inputs" # $_CONTRACT_$
  res = []
  for ele in test_list:
    N = len(ele)
    res.append(tuple(list(ele)[K: N - K]))
  return res 



assert trim_tuple([(5, 3, 2, 1, 4), (3, 4, 9, 2, 1),(9, 1, 2, 3, 5), (4, 8, 2, 1, 7)], 2) == [(2,), (9,), (2,), (2,)]
assert trim_tuple([(5, 3, 2, 1, 4), (3, 4, 9, 2, 1), (9, 1, 2, 3, 5), (4, 8, 2, 1, 7)], 1) == [(3, 2, 1), (4, 9, 2), (1, 2, 3), (8, 2, 1)]
assert trim_tuple([(7, 8, 4, 9), (11, 8, 12, 4),(4, 1, 7, 8), (3, 6, 9, 7)], 1) == [(8, 4), (8, 12), (1, 7), (6, 9)]

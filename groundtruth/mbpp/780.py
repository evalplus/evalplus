"""
Write a function to find the combinations of sums with tuples in the given tuple list. https://www.geeksforgeeks.org/python-combinations-of-sum-with-tuples-in-tuple-list/
"""

from itertools import combinations 
def find_combinations(test_list):
  assert isinstance(test_list, list), "invalid inputs" # $_CONTRACT_$
  assert len(test_list) > 0, "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(t, tuple) for t in test_list), "invalid inputs" # $_CONTRACT_$
  assert all(len(t) == len(test_list[0]) for t in test_list), "invalid inputs" # $_CONTRACT_$))
  assert all(isinstance(x, (int, float)) for t in test_list for x in t), "invalid inputs" # $_CONTRACT_$
  return [tuple(map(sum, zip(*t))) for t in combinations(test_list, 2)]



assert find_combinations([(1, 2, 3), (3, 4, 5)]) == [(4, 6, 8)]
assert find_combinations([(2, 4), (6, 7), (5, 1), (6, 10)]) == [(8, 11), (7, 5), (8, 14), (11, 8), (12, 17), (11, 11)]
assert find_combinations([(3, 5), (7, 8), (6, 2), (7, 11)]) == [(10, 13), (9, 7), (10, 16), (13, 10), (14, 19), (13, 13)]
assert find_combinations([(4, 6), (8, 9), (7, 3), (8, 12)]) == [(12, 15), (11, 9), (12, 18), (15, 12), (16, 21), (15, 15)]

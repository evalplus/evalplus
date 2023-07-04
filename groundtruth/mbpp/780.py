"""
Write a function to find the combinations of sums with tuples in the given tuple list. https://www.geeksforgeeks.org/python-combinations-of-sum-with-tuples-in-tuple-list/
"""

from itertools import combinations 
def find_combinations(test_list):
  assert isinstance(test_list, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, tuple) for x in test_list), "invalid inputs" # $_CONTRACT_$
  assert all(len(x) == 2 for x in test_list), "invalid inputs" # $_CONTRACT_$))
  assert all(isinstance(x[0], (int, float)) for x in test_list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x[1], (int, float)) for x in test_list), "invalid inputs" # $_CONTRACT_$
  res = [(b1 + a1, b2 + a2) for (a1, a2), (b1, b2) in combinations(test_list, 2)]
  return (res) 



assert find_combinations([(2, 4), (6, 7), (5, 1), (6, 10)]) == [(8, 11), (7, 5), (8, 14), (11, 8), (12, 17), (11, 11)]
assert find_combinations([(3, 5), (7, 8), (6, 2), (7, 11)]) == [(10, 13), (9, 7), (10, 16), (13, 10), (14, 19), (13, 13)]
assert find_combinations([(4, 6), (8, 9), (7, 3), (8, 12)]) == [(12, 15), (11, 9), (12, 18), (15, 12), (16, 21), (15, 15)]

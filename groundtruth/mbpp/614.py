"""
Write a function to find the cumulative sum of all the values that are present in the given tuple list.
"""

def cummulative_sum(test_list):
  assert isinstance(test_list, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(el, tuple) for el in test_list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(el, (int, float)) for el in sum(test_list, ())), "invalid inputs" # $_CONTRACT_$
  return sum(map(sum, test_list))



assert cummulative_sum([(1, 3), (5, 6, 7), (2, 6)]) == 30
assert cummulative_sum([(2, 4), (6, 7, 8), (3, 7)]) == 37
assert cummulative_sum([(3, 5), (7, 8, 9), (4, 8)]) == 44

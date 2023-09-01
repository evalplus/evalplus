"""
Write a function to find the dissimilar elements in the given two tuples.
"""

def find_dissimilar(test_tup1, test_tup2):
  assert isinstance(test_tup1, tuple), "invalid inputs" # $_CONTRACT_$
  assert isinstance(test_tup2, tuple), "invalid inputs" # $_CONTRACT_$
  return tuple(set(test_tup1) ^ set(test_tup2))



assert find_dissimilar((3, 4, 5, 6), (5, 7, 4, 10)) == (3, 6, 7, 10)
assert find_dissimilar((1, 2, 3, 4), (7, 2, 3, 9)) == (1, 4, 7, 9)
assert find_dissimilar((21, 11, 25, 26), (26, 34, 21, 36)) == (34, 36, 11, 25)

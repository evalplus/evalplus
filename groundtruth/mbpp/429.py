"""
Write a function to extract the elementwise and tuples from the given two tuples.
"""

def and_tuples(test_tup1, test_tup2):
  assert isinstance(test_tup1, tuple), "invalid inputs" # $_CONTRACT_$
  assert isinstance(test_tup2, tuple), "invalid inputs" # $_CONTRACT_$
  assert len(test_tup1) == len(test_tup2), "invalid inputs" # $_CONTRACT_$
  return tuple(x & y for x, y in zip(test_tup1, test_tup2))



assert and_tuples((10, 4, 6, 9), (5, 2, 3, 3)) == (0, 0, 2, 1)
assert and_tuples((1, 2, 3, 4), (5, 6, 7, 8)) == (1, 2, 3, 0)
assert and_tuples((8, 9, 11, 12), (7, 13, 14, 17)) == (0, 9, 10, 0)

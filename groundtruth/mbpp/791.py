"""
Write a function to remove tuples from the given tuple.
"""

def remove_nested(test_tup):
  assert isinstance(test_tup, tuple), "invalid inputs" # $_CONTRACT_$
  return tuple(e for e in test_tup if not isinstance(e, tuple))



assert remove_nested((1, 5, 7, (4, 6), 10)) == (1, 5, 7, 10)
assert remove_nested((2, 6, 8, (5, 7), 11)) == (2, 6, 8, 11)
assert remove_nested((3, 7, 9, (6, 8), 12)) == (3, 7, 9, 12)
assert remove_nested((3, 7, 9, (6, 8), (5,12), 12)) == (3, 7, 9, 12)

"""
Write a function to find the pairwise addition of the neighboring elements of the given tuple.
"""

def add_pairwise(test_tup):
  assert isinstance(test_tup, tuple), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, (int, float)) for x in test_tup), "invalid inputs" # $_CONTRACT_$
  res = tuple(i + j for i, j in zip(test_tup, test_tup[1:]))
  return (res) 



assert add_pairwise((1, 5, 7, 8, 10)) == (6, 12, 15, 18)
assert add_pairwise((2, 6, 8, 9, 11)) == (8, 14, 17, 20)
assert add_pairwise((3, 7, 9, 10, 12)) == (10, 16, 19, 22)

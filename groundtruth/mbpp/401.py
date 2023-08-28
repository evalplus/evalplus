"""
Write a function to perform index wise addition of tuple elements in the given two nested tuples.
"""

def add_nested_tuples(test_tup1, test_tup2):
  assert isinstance(test_tup1, tuple), "invalid inputs" # $_CONTRACT_$
  assert isinstance(test_tup2, tuple), "invalid inputs" # $_CONTRACT_$
  assert len(test_tup1) > 0, "invalid inputs" # $_CONTRACT_$
  assert len(test_tup2) > 0, "invalid inputs" # $_CONTRACT_$
  assert len(test_tup1) == len(test_tup2), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(ele, tuple) for ele in test_tup1), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(ele, tuple) for ele in test_tup2), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(ele, (int, float)) for tup in test_tup1 for ele in tup), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(ele, (int, float)) for tup in test_tup2 for ele in tup), "invalid inputs" # $_CONTRACT_$
  return tuple(tuple(a + b for a, b in zip(tup1, tup2))
    for tup1, tup2 in zip(test_tup1, test_tup2))



assert add_nested_tuples(((1, 3), (4, 5), (2, 9), (1, 10)), ((6, 7), (3, 9), (1, 1), (7, 3))) == ((7, 10), (7, 14), (3, 10), (8, 13))
assert add_nested_tuples(((2, 4), (5, 6), (3, 10), (2, 11)), ((7, 8), (4, 10), (2, 2), (8, 4))) == ((9, 12), (9, 16), (5, 12), (10, 15))
assert add_nested_tuples(((3, 5), (6, 7), (4, 11), (3, 12)), ((8, 9), (5, 11), (3, 3), (9, 5))) == ((11, 14), (11, 18), (7, 14), (12, 17))

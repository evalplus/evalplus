"""
Write a function which given a matrix represented as a list of lists returns the max of the n'th column.
"""

def max_of_nth(test_list, N):
  assert isinstance(test_list, list), "invalid inputs" # $_CONTRACT_$
  assert len(test_list) > 0, "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(row, list) for row in test_list), "invalid inputs" # $_CONTRACT_$
  assert len(test_list[0]) > 0, "invalid inputs" # $_CONTRACT_$
  assert all(len(row) == len(test_list[0]) for row in test_list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(item, (int, float)) for row in test_list for item in row), "invalid inputs" # $_CONTRACT_$
  assert N < len(test_list[0]), "invalid inputs" # $_CONTRACT_$
  return max([sub[N] for sub in test_list])



assert max_of_nth([[5, 6, 7], [1, 3, 5], [8, 9, 19]], 2) == 19
assert max_of_nth([[6, 7, 8], [2, 4, 6], [9, 10, 20]], 1) == 10
assert max_of_nth([[7, 8, 9], [3, 5, 7], [10, 11, 21]], 1) == 11

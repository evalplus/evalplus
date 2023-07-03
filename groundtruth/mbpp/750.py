"""
Write a function to add the given tuple to the given list.
"""

def add_tuple(test_list, test_tup):
  assert isinstance(test_list, list), "invalid inputs" # $_CONTRACT_$
  assert isinstance(test_tup, tuple), "invalid inputs" # $_CONTRACT_$
  test_list += test_tup
  return test_list



assert add_tuple([5, 6, 7], (9, 10)) == [5, 6, 7, 9, 10]
assert add_tuple([6, 7, 8], (10, 11)) == [6, 7, 8, 10, 11]
assert add_tuple([7, 8, 9], (11, 12)) == [7, 8, 9, 11, 12]

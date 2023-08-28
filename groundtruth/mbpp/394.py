"""
Write a function to check if given tuple contains no duplicates.
"""

def check_distinct(test_tup):
  assert isinstance(test_tup, tuple), "invalid inputs" # $_CONTRACT_$
  return len(test_tup) == len(set(test_tup))



assert check_distinct((1, 4, 5, 6, 1, 4)) == False
assert check_distinct((1, 4, 5, 6)) == True
assert check_distinct((2, 3, 4, 5, 6)) == True

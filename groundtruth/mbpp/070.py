"""
Write a function to find whether all the given tuples have equal length or not.
"""

def find_equal_tuple(Input):
  k = 0 if not Input else len(Input[0])
  flag = 1
  for tuple in Input:
    if len(tuple) != k:
      flag = 0
      break
  return flag
def get_equal(Input):
  assert isinstance(Input, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(item, tuple) for item in Input), "invalid inputs" # $_CONTRACT_$
  return find_equal_tuple(Input) == 1



assert get_equal([(11, 22, 33), (44, 55, 66)]) == True
assert get_equal([(1, 2, 3), (4, 5, 6, 7)]) == False
assert get_equal([(1, 2), (3, 4)]) == True

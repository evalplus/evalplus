"""
Write a function to check if the given tuple has any none value or not.
"""

def check_none(test_tup):
  res = any(map(lambda ele: ele is None, test_tup))
  return res 



assert check_none((10, 4, 5, 6, None)) == True
assert check_none((7, 8, 9, 11, 14)) == False
assert check_none((1, 2, 3, 4, None)) == True

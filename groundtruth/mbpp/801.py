"""
Write a python function to count the number of equal numbers from three given integers.
"""

def test_three_equal(x,y,z):
  assert isinstance(x, int), "invalid inputs" # $_CONTRACT_$
  assert isinstance(y, int), "invalid inputs" # $_CONTRACT_$
  assert isinstance(z, int), "invalid inputs" # $_CONTRACT_$
  result = set([x,y,z])
  if len(result) == 3:
    return 0
  elif len(result) == 2:
    return 2
  else:
    return 3



assert test_three_equal(1,1,1) == 3
assert test_three_equal(-1,-2,-3) == 0
assert test_three_equal(1,2,2) == 2

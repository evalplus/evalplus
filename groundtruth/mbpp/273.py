"""
Write a function that takes in two tuples and subtracts the elements of the first tuple by the elements of the second tuple with the same index.
"""

def substract_elements(test_tup1, test_tup2):
  assert isinstance(test_tup1, tuple), "invalid inputs" # $_CONTRACT_$
  assert isinstance(test_tup2, tuple), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, (int, float)) for x in test_tup1), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, (int, float)) for x in test_tup2), "invalid inputs" # $_CONTRACT_$
  res = tuple(map(lambda i, j: i - j, test_tup1, test_tup2))
  return (res) 



assert substract_elements((10, 4, 5), (2, 5, 18)) == (8, -1, -13)
assert substract_elements((11, 2, 3), (24, 45 ,16)) == (-13, -43, -13)
assert substract_elements((7, 18, 9), (10, 11, 12)) == (-3, 7, -3)

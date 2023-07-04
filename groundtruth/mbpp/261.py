"""
Write a function that takes in two tuples and performs mathematical division operation element-wise across the given tuples.
"""

def division_elements(test_tup1, test_tup2):
  assert isinstance(test_tup1, tuple), "invalid inputs" # $_CONTRACT_$
  assert isinstance(test_tup2, tuple), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(ele, (int, float)) for ele in test_tup1), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(ele, (int, float)) and ele != 0 for ele in test_tup2), "invalid inputs" # $_CONTRACT_$
  res = tuple(ele1 // ele2 for ele1, ele2 in zip(test_tup1, test_tup2))
  return (res) 



assert division_elements((10, 4, 6, 9),(5, 2, 3, 3)) == (2, 2, 2, 3)
assert division_elements((12, 6, 8, 16),(6, 3, 4, 4)) == (2, 2, 2, 4)
assert division_elements((20, 14, 36, 18),(5, 7, 6, 9)) == (4, 2, 6, 2)

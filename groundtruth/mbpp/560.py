"""
Write a function to find the union of the elements of two given tuples and output them in sorted order.
"""

def union_elements(test_tup1, test_tup2):
  assert isinstance(test_tup1, tuple), "invalid inputs" # $_CONTRACT_$
  assert isinstance(test_tup2, tuple), "invalid inputs" # $_CONTRACT_$
  res = tuple(set(test_tup1 + test_tup2))
  return (res) 



assert union_elements((3, 4, 5, 6),(5, 7, 4, 10) ) == (3, 4, 5, 6, 7, 10)
assert union_elements((1, 2, 3, 4),(3, 4, 5, 6) ) == (1, 2, 3, 4, 5, 6)
assert union_elements((11, 12, 13, 14),(13, 15, 16, 17) ) == (11, 12, 13, 14, 15, 16, 17)

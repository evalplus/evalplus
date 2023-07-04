"""
Write a function to convert a list to a tuple.
"""

def list_tuple(listx):
  assert isinstance(listx, list), "invalid inputs" # $_CONTRACT_$
  tuplex = tuple(listx)
  return tuplex



assert list_tuple([5, 10, 7, 4, 15, 3])==(5, 10, 7, 4, 15, 3)
assert list_tuple([2, 4, 5, 6, 2, 3, 4, 4, 7])==(2, 4, 5, 6, 2, 3, 4, 4, 7)
assert list_tuple([58,44,56])==(58,44,56)

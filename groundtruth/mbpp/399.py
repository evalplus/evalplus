"""
Write a function to perform the mathematical bitwise xor operation across the given tuples.
"""

def bitwise_xor(test_tup1, test_tup2):
  assert isinstance(test_tup1, tuple), "invalid inputs" # $_CONTRACT_$
  assert isinstance(test_tup2, tuple), "invalid inputs" # $_CONTRACT_$
  assert len(test_tup1) == len(test_tup2), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(ele, int) for ele in test_tup1), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(ele, int) for ele in test_tup2), "invalid inputs" # $_CONTRACT_$
  return tuple(ele1 ^ ele2 for ele1, ele2 in zip(test_tup1, test_tup2))



assert bitwise_xor((10, 4, 6, 9), (5, 2, 3, 3)) == (15, 6, 5, 10)
assert bitwise_xor((11, 5, 7, 10), (6, 3, 4, 4)) == (13, 6, 3, 14)
assert bitwise_xor((12, 6, 8, 11), (7, 4, 5, 6)) == (11, 2, 13, 13)

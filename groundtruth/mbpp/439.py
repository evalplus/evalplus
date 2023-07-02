"""
Write a function to join a list of multiple integers into a single integer.
"""

def multiple_to_single(L):
  assert isinstance(L, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(i, int) for i in L), "invalid inputs" # $_CONTRACT_$
  x = int("".join(map(str, L)))
  return x



assert multiple_to_single([11, 33, 50])==113350
assert multiple_to_single([-1,2,3,4,5,6])==-123456
assert multiple_to_single([10,15,20,25])==10152025

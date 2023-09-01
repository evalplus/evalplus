"""
Write a function to join a list of multiple integers into a single integer.
"""

def multiple_to_single(L):
  assert isinstance(L, list), "invalid inputs" # $_CONTRACT_$
  assert len(L) > 0, "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(item, int) for item in L), "invalid inputs" # $_CONTRACT_$
  assert all(item > 0 for item in L[1:]), "invalid inputs" # $_CONTRACT_$
  return int(''.join(map(str,L)))




assert multiple_to_single([11, 33, 50])==113350
assert multiple_to_single([-1,2,3,4,5,6])==-123456
assert multiple_to_single([10,15,20,25])==10152025

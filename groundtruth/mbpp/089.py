"""
Write a function to find the closest smaller number than n.
"""

def closest_num(N):
  assert isinstance(N, int), "invalid inputs" # $_CONTRACT_$
  return (N - 1)



assert closest_num(11) == 10
assert closest_num(7) == 6
assert closest_num(12) == 11

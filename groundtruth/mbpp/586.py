"""
Write a python function to split a list at the nth eelment and add the first part to the end.
"""

def split_Arr(l, n):
  assert isinstance(l, list), "invalid inputs" # $_CONTRACT_$
  assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
  assert 0 <= n <= len(l), "invalid inputs" # $_CONTRACT_$
  return l[n:] + l[:n]



assert split_Arr([12,10,5,6,52,36],2) == [5,6,52,36,12,10]
assert split_Arr([1,2,3,4],1) == [2,3,4,1]
assert split_Arr([0,1,2,3,4,5,6,7],3) == [3,4,5,6,7,0,1,2]

"""
Write a python function to return the negative numbers in a list.
"""

def neg_nos(list1):
  assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(i, (int, float)) for i in list1), "invalid inputs" # $_CONTRACT_$
  return [i for i in list1 if i < 0]



assert neg_nos([-1,4,5,-6]) == [-1,-6]
assert neg_nos([-1,-2,3,4]) == [-1,-2]
assert neg_nos([-7,-6,8,9]) == [-7,-6]

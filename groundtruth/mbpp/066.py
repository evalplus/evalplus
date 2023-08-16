"""
Write a python function to count the number of positive numbers in a list.
"""

def pos_count(l):
  assert isinstance(l, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(item, (int, float)) for item in l), "invalid inputs" # $_CONTRACT_$
  return len([x for x in l if x > 0])



assert pos_count([1,-2,3,-4]) == 2
assert pos_count([3,4,5,-1]) == 3
assert pos_count([1,2,3,4]) == 4

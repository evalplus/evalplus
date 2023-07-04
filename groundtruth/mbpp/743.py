"""
Write a function to rotate a given list by specified number of items to the right direction. https://www.geeksforgeeks.org/python-program-right-rotate-list-n/
"""

def rotate_right(l, m):
  assert isinstance(l, list), "invalid inputs" # $_CONTRACT_$
  assert isinstance(m, int), "invalid inputs" # $_CONTRACT_$
  assert 0 <= m <= len(l), "invalid inputs" # $_CONTRACT_$
  result =  l[-m:] + l[:-m]
  return result



assert rotate_right([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],3)==[8, 9, 10, 1, 2, 3, 4, 5, 6, 7]
assert rotate_right([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],2)==[9, 10, 1, 2, 3, 4, 5, 6, 7, 8]
assert rotate_right([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],5)==[6, 7, 8, 9, 10, 1, 2, 3, 4, 5]

"""
Write a function to check if given tuple contains no duplicates.
"""

def check_distinct(test_tup):
  res = True
  temp = set()
  for ele in test_tup:
    if ele in temp:
      res = False
      break
    temp.add(ele)
  return res 



assert check_distinct((1, 4, 5, 6, 1, 4)) == False
assert check_distinct((1, 4, 5, 6)) == True
assert check_distinct((2, 3, 4, 5, 6)) == True

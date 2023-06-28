"""
Write a function to check if a dictionary is empty
"""

def my_dict(dict1):
  if bool(dict1):
     return False
  else:
     return True



assert my_dict({10})==False
assert my_dict({11})==False
assert my_dict({})==True

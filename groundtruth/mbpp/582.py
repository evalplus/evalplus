"""
Write a function to check if a dictionary is empty
"""

def my_dict(dict1):
   assert isinstance(dict1, dict)
   return dict1 == {}



assert my_dict({10: 0})==False
assert my_dict({11: 0})==False
assert my_dict({})==True

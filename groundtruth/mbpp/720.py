"""
Write a function to add a dictionary to the tuple. The output should be a tuple.
"""

def add_dict_to_tuple(test_tup, test_dict):
  assert isinstance(test_tup, tuple), "invalid inputs" # $_CONTRACT_$
  assert isinstance(test_dict, dict), "invalid inputs" # $_CONTRACT_$
  return test_tup + (test_dict, )



assert add_dict_to_tuple((4, 5, 6), {"MSAM" : 1, "is" : 2, "best" : 3} ) == (4, 5, 6, {'MSAM': 1, 'is': 2, 'best': 3})
assert add_dict_to_tuple((1, 2, 3), {"UTS" : 2, "is" : 3, "Worst" : 4} ) == (1, 2, 3, {'UTS': 2, 'is': 3, 'Worst': 4})
assert add_dict_to_tuple((8, 9, 10), {"POS" : 3, "is" : 4, "Okay" : 5} ) == (8, 9, 10, {'POS': 3, 'is': 4, 'Okay': 5})

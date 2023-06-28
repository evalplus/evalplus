"""
Write a function to create a new tuple from the given string and list.
"""

def new_tuple(test_list, test_str):
  return tuple(test_list + [test_str])



assert new_tuple(["WEB", "is"], "best") == ('WEB', 'is', 'best')
assert new_tuple(["We", "are"], "Developers") == ('We', 'are', 'Developers')
assert new_tuple(["Part", "is"], "Wrong") == ('Part', 'is', 'Wrong')

"""
Write a function to convert tuple string to integer tuple.
"""

def tuple_str_int(test_str):
  assert isinstance(test_str, str), "invalid inputs" # $_CONTRACT_$
  assert test_str.startswith('('), "invalid inputs" # $_CONTRACT_$
  assert test_str.endswith(')'), "invalid inputs" # $_CONTRACT_$
  assert test_str.lstrip('(').rstrip(')').replace('...', '').replace(',', '').replace(' ', '').isdigit(), "invalid inputs" # $_CONTRACT_$
  return tuple(int(num) for num in test_str.replace('(', '').replace(')', '').replace('...', '').split(', '))



assert tuple_str_int("(7, 8, 9)") == (7, 8, 9)
assert tuple_str_int("(1, 2, 3)") == (1, 2, 3)
assert tuple_str_int("(4, 5, 6)") == (4, 5, 6)
assert tuple_str_int("(7, 81, 19)") == (7, 81, 19)

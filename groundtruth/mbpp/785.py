"""
Write a function to convert tuple string to integer tuple.
"""

def tuple_str_int(test_str):
  res = tuple(int(num) for num in test_str.replace('(', '').replace(')', '').replace('...', '').split(', '))
  return (res) 



assert tuple_str_int("(7, 8, 9)") == (7, 8, 9)
assert tuple_str_int("(1, 2, 3)") == (1, 2, 3)
assert tuple_str_int("(4, 5, 6)") == (4, 5, 6)
assert tuple_str_int("(7, 81, 19)") == (7, 81, 19)

"""
Write a function to find the number of elements that occurs before the tuple element in the given tuple.
"""

def count_first_elements(test_tup):
  assert isinstance(test_tup, tuple), "invalid inputs" # $_CONTRACT_$
  for count, ele in enumerate(test_tup):
    if isinstance(ele, tuple):
      break
  return (count) 



assert count_first_elements((1, 5, 7, (4, 6), 10) ) == 3
assert count_first_elements((2, 9, (5, 7), 11) ) == 2
assert count_first_elements((11, 15, 5, 8, (2, 3), 8) ) == 4

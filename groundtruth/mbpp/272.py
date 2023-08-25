"""
Write a function that takes in a list of tuples and returns a list containing the rear element of each tuple.
"""

def rear_extract(test_list):
  assert isinstance(test_list, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, tuple) and len(x) > 0 for x in test_list), "invalid inputs" # $_CONTRACT_$
  return [x[-1] for x in test_list]



assert rear_extract([(1, 'Rash', 21), (2, 'Varsha', 20), (3, 'Kil', 19)]) == [21, 20, 19]
assert rear_extract([(1, 'Sai', 36), (2, 'Ayesha', 25), (3, 'Salman', 45)]) == [36, 25, 45]
assert rear_extract([(1, 'Sudeep', 14), (2, 'Vandana', 36), (3, 'Dawood', 56)]) == [14, 36, 56]

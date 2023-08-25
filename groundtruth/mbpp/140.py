"""
Write a function to flatten the list of lists into a single set of numbers.
"""

def extract_singly(test_list):
  assert isinstance(test_list, (list, tuple)), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, (list, tuple)) for x in test_list), "invalid inputs" # $_CONTRACT_$
  assert all(all(isinstance(y, (int, float)) for y in x) for x in test_list), "invalid inputs" # $_CONTRACT_$
  return set([item for sublist in test_list for item in sublist])



assert extract_singly([(3, 4, 5), (4, 5, 7), (1, 4)]) == set([3, 4, 5, 7, 1])
assert extract_singly([(1, 2, 3), (4, 2, 3), (7, 8)]) == set([1, 2, 3, 4, 7, 8])
assert extract_singly([(7, 8, 9), (10, 11, 12), (10, 11)]) == set([7, 8, 9, 10, 11, 12])

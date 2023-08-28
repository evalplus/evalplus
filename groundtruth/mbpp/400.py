"""
Write a function to extract the number of unique tuples in the given list.
"""

def extract_freq(test_list):
  assert isinstance(test_list, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(ele, tuple) for ele in test_list), "invalid inputs" # $_CONTRACT_$
  return len(set(tuple(sorted(l)) for l in test_list))



assert extract_freq([(3, 4), (1, 2), (4, 3), (5, 6)] ) == 3
assert extract_freq([(4, 15), (2, 3), (5, 4), (6, 7)] ) == 4
assert extract_freq([(5, 16), (2, 3), (6, 5), (6, 9)] ) == 4

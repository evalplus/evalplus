"""
Write a function to extract only the rear index element of each string in the given tuple.
"""

def extract_rear(test_tuple):
  assert isinstance(test_tuple, tuple), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(ele, str) for ele in test_tuple), "invalid inputs" # $_CONTRACT_$
  assert all(len(ele) > 0 for ele in test_tuple), "invalid inputs" # $_CONTRACT_$
  return [ele[-1] for ele in test_tuple]




assert extract_rear(('Mers', 'for', 'Vers') ) == ['s', 'r', 's']
assert extract_rear(('Avenge', 'for', 'People') ) == ['e', 'r', 'e']
assert extract_rear(('Gotta', 'get', 'go') ) == ['a', 't', 'o']

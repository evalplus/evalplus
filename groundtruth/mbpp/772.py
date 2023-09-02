"""
Write a function to remove all the words with k length in the given string.
"""

def remove_length(test_str, K):
  assert isinstance(test_str, str), "invalid inputs" # $_CONTRACT_$
  assert isinstance(K, int), "invalid inputs" # $_CONTRACT_$
  return ' '.join([i for i in test_str.split() if len(i) != K])



assert remove_length('The person is most value tet', 3) == 'person is most value'
assert remove_length('If you told me about this ok', 4) == 'If you me about ok'
assert remove_length('Forces of darkeness is come into the play', 4) == 'Forces of darkeness is the'

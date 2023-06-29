"""
Write a function to find tuples which have all elements divisible by k from the given list of tuples.
"""

def find_tuples(test_list, K):
  assert isinstance(test_list, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(item, tuple) for item in test_list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(item, int) for tuple in test_list for item in tuple), "invalid inputs" # $_CONTRACT_$
  assert isinstance(K, int), "invalid inputs" # $_CONTRACT_$
  res = [sub for sub in test_list if all(ele % K == 0 for ele in sub)]
  return res



assert find_tuples([(6, 24, 12), (7, 9, 6), (12, 18, 21)], 6) == [(6, 24, 12)]
assert find_tuples([(5, 25, 30), (4, 2, 3), (7, 8, 9)], 5) == [(5, 25, 30)]
assert find_tuples([(7, 9, 16), (8, 16, 4), (19, 17, 18)], 4) == [(8, 16, 4)]

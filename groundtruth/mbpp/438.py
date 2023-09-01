"""
Write a function to count bidirectional tuple pairs.
"""

def count_bidirectional(test_list):
  assert isinstance(test_list, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(ele, tuple) for ele in test_list), "invalid inputs" # $_CONTRACT_$
  assert all(len(ele) == 2 for ele in test_list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(ele[0], int) for ele in test_list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(ele[1], int) for ele in test_list), "invalid inputs" # $_CONTRACT_$
  return sum(test_list.count(l[::-1]) for l in test_list) / 2



assert count_bidirectional([(5, 6), (1, 2), (6, 5), (9, 1), (6, 5), (2, 1)] ) == 3
assert count_bidirectional([(5, 6), (1, 3), (6, 5), (9, 1), (6, 5), (2, 1)] ) == 2
assert count_bidirectional([(5, 6), (1, 2), (6, 5), (9, 2), (6, 5), (2, 1)] ) == 3

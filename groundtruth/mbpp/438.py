"""
Write a function to count bidirectional tuple pairs.
"""

def count_bidirectional(test_list):
  assert isinstance(test_list, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(ele, tuple) for ele in test_list), "invalid inputs" # $_CONTRACT_$
  assert all(len(ele) == 2 for ele in test_list), "invalid inputs" # $_CONTRACT_$
  res = 0
  for idx in range(0, len(test_list)):
    for iidx in range(idx + 1, len(test_list)):
      if test_list[iidx][0] == test_list[idx][1] and test_list[idx][1] == test_list[iidx][0]:
        res += 1
  return res



assert count_bidirectional([(5, 6), (1, 2), (6, 5), (9, 1), (6, 5), (2, 1)] ) == 3
assert count_bidirectional([(5, 6), (1, 3), (6, 5), (9, 1), (6, 5), (2, 1)] ) == 2
assert count_bidirectional([(5, 6), (1, 2), (6, 5), (9, 2), (6, 5), (2, 1)] ) == 4

"""
Write a function to find the maximum difference between available pairs in the given tuple list.
"""

def max_difference(test_list):
  assert isinstance(test_list, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(item, tuple) and len(item) == 2 for item in test_list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(a, (int, float)) and isinstance(b, (int, float)) for a, b in test_list), "invalid inputs" # $_CONTRACT_$
  temp = [abs(b - a) for a, b in test_list]
  res = max(temp)
  return (res) 



assert max_difference([(3, 5), (1, 7), (10, 3), (1, 2)]) == 7
assert max_difference([(4, 6), (2, 17), (9, 13), (11, 12)]) == 15
assert max_difference([(12, 35), (21, 27), (13, 23), (41, 22)]) == 23

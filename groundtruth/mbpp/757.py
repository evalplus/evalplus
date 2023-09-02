"""
Write a function to count the pairs of reverse strings in the given string list. https://www.geeksforgeeks.org/python-program-to-count-the-pairs-of-reverse-strings/
"""

def count_reverse_pairs(test_list):
  assert isinstance(test_list, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, str) for x in test_list), "invalid inputs" # $_CONTRACT_$
  return sum(test_list[i+1:].count(s[::-1]) for i, s in enumerate(test_list))



assert count_reverse_pairs(["julia", "best", "tseb", "for", "ailuj"])== 2
assert count_reverse_pairs(["geeks", "best", "for", "skeeg"]) == 1
assert count_reverse_pairs(["makes", "best", "sekam", "for", "rof"]) == 2

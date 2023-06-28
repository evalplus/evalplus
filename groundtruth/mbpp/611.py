"""
Write a function which given a matrix represented as a list of lists returns the max of the n'th column.
"""

def max_of_nth(test_list, N):
  res = max([sub[N] for sub in test_list])
  return (res) 



assert max_of_nth([[5, 6, 7], [1, 3, 5], [8, 9, 19]], 2) == 19
assert max_of_nth([[6, 7, 8], [2, 4, 6], [9, 10, 20]], 1) == 10
assert max_of_nth([[7, 8, 9], [3, 5, 7], [10, 11, 21]], 1) == 11

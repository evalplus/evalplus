"""
Write a function that takes as input a tuple of numbers (t_1,...,t_{N+1}) and returns a tuple of length N where the i-th element of the tuple is equal to t_i * t_{i+1}.
"""

def multiply_elements(test_tup):
  assert isinstance(test_tup, tuple), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, (int, float)) for x in test_tup), "invalid inputs" # $_CONTRACT_$
  res = tuple(i * j for i, j in zip(test_tup, test_tup[1:]))
  return (res) 



assert multiply_elements((1, 5, 7, 8, 10)) == (5, 35, 56, 80)
assert multiply_elements((2, 4, 5, 6, 7)) == (8, 20, 30, 42)
assert multiply_elements((12, 13, 14, 9, 15)) == (156, 182, 126, 135)
assert multiply_elements((12,)) == ()

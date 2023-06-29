"""
Write a function to find nth centered hexagonal number.
"""

def centered_hexagonal_number(n):
  assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
  assert n > 0, "invalid inputs" # $_CONTRACT_$
  return 3 * n * (n - 1) + 1



assert centered_hexagonal_number(10) == 271
assert centered_hexagonal_number(2) == 7
assert centered_hexagonal_number(9) == 217

"""
Write a function that takes in an array and an integer n, and re-arranges the first n elements of the given array so that all negative elements appear before positive ones, and where the relative order among negative and positive elements is preserved.
"""

def re_arrange_array(arr, n):
  assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, int) for x in arr), "invalid inputs" # $_CONTRACT_$
  assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
  assert 0 <= n <= len(arr), "invalid inputs" # $_CONTRACT_$
  negatives = [x for x in arr[:n] if x < 0]
  positives = [x for x in arr[:n] if x >= 0]
  return negatives + positives + arr[n:]



assert re_arrange_array([-1, 2, -3, 4, 5, 6, -7, 8, 9], 9) == [-1, -3, -7, 2, 4, 5, 6, 8, 9]
assert re_arrange_array([12, -14, -26, 13, 15], 5) == [-14, -26, 12, 13, 15]
assert re_arrange_array([10, 24, 36, -42, -39, -78, 85], 7) == [-42, -39, -78, 10, 24, 36, 85]

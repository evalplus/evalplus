"""
Write a function to find the maximum product formed by multiplying numbers of an increasing subsequence of that array.
"""

def max_product(arr):   
  assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, (int, float)) for x in arr), "invalid inputs" # $_CONTRACT_$
  assert len(arr) > 0, "invalid inputs" # $_CONTRACT_$
  # record the correspond ending element to maintain the increasing subsequence
  ret = max_ending = min_ending = (arr[0], arr[0])
  for n in arr[1:]:
    if n > max_ending[1]:
      max_ending = max((max_ending[0] * n, n), max_ending, key=lambda x: x[0])
    else:
      max_ending = (n, n)
    if n > min_ending[1]:
      min_ending = min((min_ending[0] * n, n), min_ending, key=lambda x: x[0])
    else:
      min_ending = (n, n)
    ret = max(ret, max_ending, min_ending, key=lambda x: x[0])
  return ret[0]




assert max_product([3, 100, 4, 5, 150, 6]) == 3000
assert max_product([4, 42, 55, 68, 80]) == 50265600
assert max_product([10, 22, 9, 33, 21, 50, 41, 60]) == 2460

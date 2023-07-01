"""
Write a function to find the kth element in the given array using 1-based indexing.
"""

def kth_element(arr, k):
  assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
  assert isinstance(k, int), "invalid inputs" # $_CONTRACT_$ 
  assert len(arr) >= k >= 1, "invalid inputs" # $_CONTRACT_$
  return arr[k-1]



assert kth_element([12,3,5,7,19], 2) == 3
assert kth_element([17,24,8,23], 3) == 8
assert kth_element([16,21,25,36,4], 4) == 36

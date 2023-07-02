"""
Write a function to find the median of two sorted lists of same size.
"""

def get_median(arr1, arr2, n):
  assert isinstance(arr1, list), "invalid inputs" # $_CONTRACT_$
  assert isinstance(arr2, list), "invalid inputs" # $_CONTRACT_$
  assert 0 <= n <= min(len(arr1), len(arr2)), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(el, (int, float)) for el in arr1 + arr2), "invalid inputs" # $_CONTRACT_$
  assert all(x <= y for x, y in zip(arr1[0:n], arr1[1:n])), "invalid inputs" # $_CONTRACT_$
  assert all(x <= y for x, y in zip(arr2[0:n], arr2[1:n])), "invalid inputs" # $_CONTRACT_$
  i = 0
  j = 0
  m1 = -1
  m2 = -1
  count = 0
  while count < n + 1:
    count += 1
    if i == n:
      m1 = m2
      m2 = arr2[0]
      break
    elif j == n:
      m1 = m2
      m2 = arr1[0]
      break
    if arr1[i] <= arr2[j]:
      m1 = m2
      m2 = arr1[i]
      i += 1
    else:
      m1 = m2
      m2 = arr2[j]
      j += 1
  return (m1 + m2)/2



assert get_median([1, 12, 15, 26, 38], [2, 13, 17, 30, 45], 5) == 16.0
assert get_median([2, 4, 8, 9], [7, 13, 19, 28], 4) == 8.5
assert get_median([3, 6, 14, 23, 36, 42], [2, 18, 27, 39, 49, 55], 6) == 25.0

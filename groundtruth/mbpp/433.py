"""
Write a function to check whether the entered number is greater than the elements of the given array.
"""

def check_greater(arr, number):
  assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(el, (int, float)) for el in arr), "invalid inputs" # $_CONTRACT_$
  assert isinstance(number, (int, float)), "invalid inputs" # $_CONTRACT_$
  return all(number > el for el in arr)



assert check_greater([1, 2, 3, 4, 5], 4) == False
assert check_greater([2, 3, 4, 5, 6], 8) == True
assert check_greater([9, 7, 4, 8, 6, 1], 11) == True

"""
Write a function to check whether the entered number is greater than the elements of the given array.
"""

def check_greater(arr, number):
  arr.sort()
  return number > arr[-1]



assert check_greater([1, 2, 3, 4, 5], 4) == False
assert check_greater([2, 3, 4, 5, 6], 8) == True
assert check_greater([9, 7, 4, 8, 6, 1], 11) == True

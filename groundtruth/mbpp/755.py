"""
Write a function to find the second smallest number in a list.
"""

def second_smallest(numbers):
  assert isinstance(numbers, list), "invalid inputs" # $_CONTRACT_$
  unique_numbers = list(set(numbers))
  unique_numbers.sort()
  if len(unique_numbers) < 2:
    return None
  else:
    return unique_numbers[1]



assert second_smallest([1, 2, -8, -2, 0, -2])==-2
assert second_smallest([1, 1, -0.5, 0, 2, -2, -2])==-0.5
assert second_smallest([2,2])==None
assert second_smallest([2,2,2])==None

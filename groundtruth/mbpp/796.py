"""
Write function to find the sum of all items in the given dictionary.
"""

def return_sum(dict):
  sum = 0
  for i in dict.values():
    sum = sum + i
  return sum



assert return_sum({'a': 100, 'b':200, 'c':300}) == 600
assert return_sum({'a': 25, 'b':18, 'c':45}) == 88
assert return_sum({'a': 36, 'b':39, 'c':49}) == 124

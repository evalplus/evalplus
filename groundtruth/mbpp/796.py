"""
Write function to find the sum of all items in the given dictionary.
"""

def return_sum(d):
  assert isinstance(d, dict), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, (int, float)) for x in d.values()), "invalid inputs" # $_CONTRACT_$
  sum = 0
  for i in d.values():
    sum = sum + i
  return sum



assert return_sum({'a': 100, 'b':200, 'c':300}) == 600
assert return_sum({'a': 25, 'b':18, 'c':45}) == 88
assert return_sum({'a': 36, 'b':39, 'c':49}) == 124

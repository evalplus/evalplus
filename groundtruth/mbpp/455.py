"""
Write a function to check whether the given month number contains 31 days or not.
"""

def check_monthnumb_number(monthnum2):
  assert isinstance(monthnum2, int), "invalid inputs" # $_CONTRACT_$
  assert 1 <= monthnum2 <= 12, "invalid inputs" # $_CONTRACT_$
  return monthnum2 in [1, 3, 5, 7, 8, 10, 12]




assert check_monthnumb_number(5)==True
assert check_monthnumb_number(2)==False
assert check_monthnumb_number(6)==False

"""
Write a function to check whether the given month number contains 30 days or not. Months are given as number from 1 to 12.
"""

def check_monthnumber_number(monthnum3):
  return monthnum3==4 or monthnum3==6 or monthnum3==9 or monthnum3==11



assert check_monthnumber_number(6)==True
assert check_monthnumber_number(2)==False
assert check_monthnumber_number(12)==False

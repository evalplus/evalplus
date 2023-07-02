"""
Write a function to check whether the given month number contains 31 days or not.
"""

def check_monthnumb_number(monthnum2):
  assert isinstance(monthnum2, int), "invalid inputs" # $_CONTRACT_$
  if(monthnum2==1 or monthnum2==3 or monthnum2==5 or monthnum2==7 or monthnum2==8 or monthnum2==10 or monthnum2==12):
    return True
  else:
    return False



assert check_monthnumb_number(5)==True
assert check_monthnumb_number(2)==False
assert check_monthnumb_number(6)==False

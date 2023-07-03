"""
Write a python function to count number of digits in a given string.
"""

def number_ctr(s):
      assert isinstance(s, str), "invalid inputs" # $_CONTRACT_$
      number_ctr= 0
      for i in range(len(s)):
          if s[i] >= '0' and s[i] <= '9': number_ctr += 1     
      return  number_ctr



assert number_ctr('program2bedone') == 1
assert number_ctr('3wonders') == 1
assert number_ctr('123') == 3
assert number_ctr('3wond-1ers2') == 3

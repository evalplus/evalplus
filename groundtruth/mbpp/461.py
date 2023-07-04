"""
Write a python function to count the upper case characters in a given string.
"""

def upper_ctr(str1):
    assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
    upper_ctr = 0
    for i in range(len(str1)):
          if str1[i] >= 'A' and str1[i] <= 'Z': upper_ctr += 1
          return upper_ctr



assert upper_ctr('PYthon') == 1
assert upper_ctr('BigData') == 1
assert upper_ctr('program') == 0

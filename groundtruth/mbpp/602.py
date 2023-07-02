"""
Write a python function to find the first repeated character in a given string.
"""

def first_repeated_char(str1):
  assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$I
  for index,c in enumerate(str1):
    if str1[:index+1].count(c) > 1:
      return c



assert first_repeated_char("abcabc") == "a"
assert first_repeated_char("abc") == None
assert first_repeated_char("123123") == "1"

"""
Write a python function to find the first non-repeated character in a given string.
"""

def first_non_repeating_character(str1):
  assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
  assert len(str1) > 0, "invalid inputs" # $_CONTRACT_$
  for ch in str1:
    if str1.count(ch) == 1:
      return ch
  return None



assert first_non_repeating_character("abcabc") == None
assert first_non_repeating_character("abc") == "a"
assert first_non_repeating_character("ababc") == "c"

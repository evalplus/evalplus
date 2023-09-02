"""
Write a function to count those characters which have vowels as their neighbors in the given string.
"""

def count_vowels(test_str):
  assert isinstance(test_str, str), "invalid inputs" # $_CONTRACT_$
  cnt = 0
  vowels = 'aeiou'
  if test_str[0] not in vowels and test_str[1] in vowels:
    cnt += 1
  if test_str[-1] not in vowels and test_str[-2] in vowels:
    cnt += 1
  for i in range(1, len(test_str) - 1):
    if test_str[i] not in vowels and (test_str[i - 1] in vowels or test_str[i + 1] in vowels):
      cnt += 1
  return cnt 



assert count_vowels('bestinstareels') == 7
assert count_vowels('partofthejourneyistheend') == 12
assert count_vowels('amazonprime') == 5

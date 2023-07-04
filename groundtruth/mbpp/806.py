"""
Write a function to find maximum run of uppercase characters in the given string.
"""

def max_run_uppercase(test_str):
  assert isinstance(test_str, str), "invalid inputs" # $_CONTRACT_$
  assert len(test_str) > 0, "invalid inputs" # $_CONTRACT_$
  cnt = 0
  res = 0
  for idx in range(0, len(test_str)):
    if test_str[idx].isupper():
      cnt += 1
    else:
      res = cnt
      cnt = 0
  if test_str[len(test_str) - 1].isupper():
    res = cnt
  return (res)



assert max_run_uppercase('GeMKSForGERksISBESt') == 5
assert max_run_uppercase('PrECIOusMOVemENTSYT') == 6
assert max_run_uppercase('GooGLEFluTTER') == 4

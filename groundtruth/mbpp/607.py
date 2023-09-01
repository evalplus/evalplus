"""
Write a function to search a string for a regex pattern. The function should return the matching subtring, a start index and an end index.
"""

import re

def find_literals(text, pattern):
  assert isinstance(text, str), "invalid inputs" # $_CONTRACT_$
  assert isinstance(pattern, str), "invalid inputs" # $_CONTRACT_$
  match = re.search(pattern, text)
  if match is None:
    return None
  s = match.start()
  e = match.end()
  return (match.re.pattern, s, e)



assert find_literals('The quick brown fox jumps over the lazy dog.', 'fox') == ('fox', 16, 19)
assert find_literals('Its been a very crazy procedure right', 'crazy') == ('crazy', 16, 21)
assert find_literals('Hardest choices required strongest will', 'will') == ('will', 35, 39)

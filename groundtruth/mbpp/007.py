"""
Write a function to find all words which are at least 4 characters long in a string.
"""

import re
def find_char_long(text):
  return (re.findall(r"\b\w{4,}\b", text))



assert set(find_char_long('Please move back to stream')) == set(['Please', 'move', 'back', 'stream'])
assert set(find_char_long('Jing Eco and Tech')) == set(['Jing', 'Tech'])
assert set(find_char_long('Jhingai wulu road Zone 3')) == set(['Jhingai', 'wulu', 'road', 'Zone'])

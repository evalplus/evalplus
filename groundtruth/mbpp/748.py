"""
Write a function to put spaces between words starting with capital letters in a given string.
"""

import re
def capital_words_spaces(str1):
  assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
  return re.sub(r"(\w)([A-Z])", r"\1 \2", str1)



assert capital_words_spaces("Python") == 'Python'
assert capital_words_spaces("PythonProgrammingExamples") == 'Python Programming Examples'
assert capital_words_spaces("GetReadyToBeCodingFreak") == 'Get Ready To Be Coding Freak'

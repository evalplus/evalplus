"""
Write a function to sum the length of the names of a given list of names after removing the names that start with a lowercase letter.
"""

def sample_nam(sample_names):
  assert isinstance(sample_names, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, str) for x in sample_names), "invalid inputs" # $_CONTRACT_$
  sample_names=list(filter(lambda el:el[0].isupper() and el[1:].islower(),sample_names))
  return len(''.join(sample_names))



assert sample_nam(['sally', 'Dylan', 'rebecca', 'Diana', 'Joanne', 'keith'])==16
assert sample_nam(["php", "res", "Python", "abcd", "Java", "aaa"])==10
assert sample_nam(["abcd", "Python", "abba", "aba"])==6

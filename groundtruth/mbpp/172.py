"""
Write a function to count the number of occurence of the string 'std' in a given string.
"""

def count_occurance(s):
  assert isinstance(s, str), "invalid inputs" # $_CONTRACT_$
  return s.count('std')



assert count_occurance("letstdlenstdporstd") == 3
assert count_occurance("truststdsolensporsd") == 1
assert count_occurance("makestdsostdworthit") == 2
assert count_occurance("stds") == 1
assert count_occurance("") == 0

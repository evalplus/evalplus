"""
Write a function to convert a tuple to a string.
"""

def tup_string(tup1):
  assert isinstance(tup1, tuple), "invalid inputs" # $_CONTRACT_$
  str =  ''.join(tup1)
  return str



assert tup_string(('e', 'x', 'e', 'r', 'c', 'i', 's', 'e', 's'))==("exercises")
assert tup_string(('p','y','t','h','o','n'))==("python")
assert tup_string(('p','r','o','g','r','a','m'))==("program")

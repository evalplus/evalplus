"""
Write a function to find the ascii value of a character.
"""

def ascii_value(k):
  assert isinstance(k, str), "invalid inputs" # $_CONTRACT_$
  assert len(k)==1, "invalid inputs" # $_CONTRACT_$
  ch=k
  return ord(ch)



assert ascii_value('A')==65
assert ascii_value('R')==82
assert ascii_value('S')==83

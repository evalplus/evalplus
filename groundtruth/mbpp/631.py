"""
Write a function to replace whitespaces with an underscore and vice versa in a given string.
"""

def replace_spaces(text):
  assert isinstance(text, str), "invalid inputs" # $_CONTRACT_$
  return "".join(" " if c == "_" else ("_" if c == " " else c) for c in text)



assert replace_spaces('Jumanji The Jungle') == 'Jumanji_The_Jungle'
assert replace_spaces('The_Avengers') == 'The Avengers'
assert replace_spaces('Fast and Furious') == 'Fast_and_Furious'

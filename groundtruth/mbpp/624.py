"""
Write a python function to convert a given string to uppercase.
"""

def is_upper(string):
  assert isinstance(string, str), "invalid inputs" # $_CONTRACT_$
  return string.upper()



assert is_upper("person") =="PERSON"
assert is_upper("final") == "FINAL"
assert is_upper("Valid") == "VALID"

"""
Write a function to check whether an element exists within a tuple.
"""

def check_tuplex(tuplex, element): 
  assert isinstance(tuplex, tuple), "invalid inputs" # $_CONTRACT_$
  return element in tuplex



assert check_tuplex(("w", 3, "r", "e", "s", "o", "u", "r", "c", "e"),'r')==True
assert check_tuplex(("w", 3, "r", "e", "s", "o", "u", "r", "c", "e"),'5')==False
assert check_tuplex(("w", 3, "r", "e", "s", "o", "u", "r", "c","e"),3)==True

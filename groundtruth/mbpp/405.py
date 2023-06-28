"""
Write a function to check whether an element exists within a tuple.
"""

def check_tuplex(tuplex,tuple1): 
  if tuple1 in tuplex:
    return True
  else:
     return False



assert check_tuplex(("w", 3, "r", "e", "s", "o", "u", "r", "c", "e"),'r')==True
assert check_tuplex(("w", 3, "r", "e", "s", "o", "u", "r", "c", "e"),'5')==False
assert check_tuplex(("w", 3, "r", "e", "s", "o", "u", "r", "c","e"),3)==True

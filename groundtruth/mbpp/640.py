"""
Write a function to remove the parenthesis and what is inbetween them from a string.
"""

import re
def remove_parenthesis(items):
 assert isinstance(items, list), "invalid inputs" # $_CONTRACT_$
 assert all(isinstance(x, str) for x in items), "invalid inputs" # $_CONTRACT_$
 for item in items:
    return (re.sub(r" ?\([^)]+\)", "", item))



assert remove_parenthesis(["python (chrome)"])==("python")
assert remove_parenthesis(["string(.abc)"])==("string")
assert remove_parenthesis(["alpha(num)"])==("alpha")

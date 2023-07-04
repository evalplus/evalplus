"""
Write a function to remove all whitespaces from a string.
"""

import re
def remove_all_spaces(text):
 assert isinstance(text, str), "invalid inputs" # $_CONTRACT_$
 return (re.sub(r'\s+', '',text))



assert remove_all_spaces('python  program')==('pythonprogram')
assert remove_all_spaces('python   programming    language')==('pythonprogramminglanguage')
assert remove_all_spaces('python                     program')==('pythonprogram')
assert remove_all_spaces('   python                     program')=='pythonprogram'

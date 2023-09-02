"""
Write a function to remove all whitespaces from a string.
"""

def remove_all_spaces(text):
 assert isinstance(text, str), "invalid inputs" # $_CONTRACT_$
 return text.replace(' ', '')



assert remove_all_spaces('python  program')==('pythonprogram')
assert remove_all_spaces('python   programming    language')==('pythonprogramminglanguage')
assert remove_all_spaces('python                     program')==('pythonprogram')
assert remove_all_spaces('   python                     program')=='pythonprogram'

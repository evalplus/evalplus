"""
Write a function to replace all spaces in the given string with '%20'.
"""

def replace_spaces(string):
  return string.replace(" ", "%20")



assert replace_spaces("My Name is Dawood") == 'My%20Name%20is%20Dawood'
assert replace_spaces("I am a Programmer") == 'I%20am%20a%20Programmer'
assert replace_spaces("I love Coding") == 'I%20love%20Coding'

"""
Write a function to convert a string to a list of strings split on the space character.
"""

def string_to_list(string): 
    assert isinstance(string, str), "invalid inputs" # $_CONTRACT_$
    return string.split(" ")



assert string_to_list("python programming")==['python','programming']
assert string_to_list("lists tuples strings")==['lists','tuples','strings']
assert string_to_list("write a program")==['write','a','program']

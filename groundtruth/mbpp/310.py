"""
Write a function to convert a given string to a tuple of characters.
"""

def string_to_tuple(str1):
    assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
    result = tuple(x for x in str1 if not x.isspace()) 
    return result



assert string_to_tuple("python 3.0")==('p', 'y', 't', 'h', 'o', 'n', '3', '.', '0')
assert string_to_tuple("item1")==('i', 't', 'e', 'm', '1')
assert string_to_tuple("15.10")==('1', '5', '.', '1', '0')

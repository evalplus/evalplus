"""
Write a function that takes in a string and character, replaces blank spaces in the string with the character, and returns the string.
"""

def replace_blank(str1, char):
    assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
    assert isinstance(char, str), "invalid inputs" # $_CONTRACT_$
    assert len(char) == 1, "invalid inputs" # $_CONTRACT_$
    return str1.replace(' ', char)



assert replace_blank("hello people",'@')==("hello@people")
assert replace_blank("python program language",'$')==("python$program$language")
assert replace_blank("blank space","-")==("blank-space")

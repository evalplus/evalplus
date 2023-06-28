"""
Write a function that takes in a string and character, replaces blank spaces in the string with the character, and returns the string.
"""

def replace_blank(str1,char):
 str2 = str1.replace(' ', char)
 return str2



assert replace_blank("hello people",'@')==("hello@people")
assert replace_blank("python program language",'$')==("python$program$language")
assert replace_blank("blank space","-")==("blank-space")

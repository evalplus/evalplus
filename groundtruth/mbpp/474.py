"""
Write a function to replace characters in a string.
"""

def replace_char(str1,ch,newch):
 str2 = str1.replace(ch, newch)
 return str2



assert replace_char("polygon",'y','l')==("pollgon")
assert replace_char("character",'c','a')==("aharaater")
assert replace_char("python",'l','a')==("python")

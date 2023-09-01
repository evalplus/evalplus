"""
Write a function to replace characters in a string.
"""

def replace_char(str1, ch, newch):
    assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
    assert isinstance(ch, str), "invalid inputs" # $_CONTRACT_$
    assert len(ch) == 1, "invalid inputs" # $_CONTRACT_$
    assert isinstance(newch, str), "invalid inputs" # $_CONTRACT_$
    assert len(newch) == 1, "invalid inputs" # $_CONTRACT_$
    return str1.replace(ch, newch)



assert replace_char("polygon",'y','l')==("pollgon")
assert replace_char("character",'c','a')==("aharaater")
assert replace_char("python",'l','a')==("python")

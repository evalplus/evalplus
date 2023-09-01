"""
Write a function to remove odd characters in a string.
"""

def remove_odd(str1):
    assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
    return str1[1::2]



assert remove_odd("python")==("yhn")
assert remove_odd("program")==("rga")
assert remove_odd("language")==("agae")

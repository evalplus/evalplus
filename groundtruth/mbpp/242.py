"""
Write a function to count the total number of characters in a string.
"""

def count_charac(str1):
    assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
    return len(str1)



assert count_charac("python programming")==18
assert count_charac("language")==8
assert count_charac("words")==5

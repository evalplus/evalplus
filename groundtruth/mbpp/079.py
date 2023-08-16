"""
Write a python function to check whether the length of the word is odd or not.
"""

def word_len(s): 
    assert isinstance(s, str), "invalid inputs" # $_CONTRACT_$
    assert s.isalpha(), "invalid inputs" # $_CONTRACT_$
    return len(s) % 2 == 1



assert word_len("Hadoop") == False
assert word_len("great") == True
assert word_len("structure") == True

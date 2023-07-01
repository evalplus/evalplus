"""
Write a python function to split a string into characters.
"""

def split(word): 
    assert isinstance(word, str), "invalid inputs" # $_CONTRACT_$
    return [char for char in word] 



assert split('python') == ['p','y','t','h','o','n']
assert split('Name') == ['N','a','m','e']
assert split('program') == ['p','r','o','g','r','a','m']

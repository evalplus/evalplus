"""
Write a function to count the number of characters in a string that occur at the same position in the string as in the English alphabet (case insensitive).
"""

def count_char_position(str1): 
    assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
    assert all(x.isalpha() for x in str1), "invalid inputs" # $_CONTRACT_$
    return sum(ord(ch.lower()) - ord('a') == i for i, ch in enumerate(str1))



assert count_char_position("xbcefg") == 2
assert count_char_position("ABcED") == 3
assert count_char_position("AbgdeF") == 5

"""
Write a function to count the number of characters in a string that occur at the same position in the string as in the English alphabet (case insensitive).
"""

def count_char_position(str1): 
    assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
    assert all(x.isalpha() for x in str1), "invalid inputs" # $_CONTRACT_$
    count_chars = 0
    for i in range(len(str1)):
        if ((i == ord(str1[i]) - ord('A')) or 
            (i == ord(str1[i]) - ord('a'))): 
            count_chars += 1
    return count_chars 



assert count_char_position("xbcefg") == 2
assert count_char_position("ABcED") == 3
assert count_char_position("AbgdeF") == 5

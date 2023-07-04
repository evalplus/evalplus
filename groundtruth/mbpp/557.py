"""
Write a function to toggle the case of all characters in a string.
"""

def toggle_string(string):
 assert isinstance(string, str), "invalid inputs" # $_CONTRACT_$
 string1 = string.swapcase()
 return string1



assert toggle_string("Python")==("pYTHON")
assert toggle_string("Pangram")==("pANGRAM")
assert toggle_string("LIttLE")==("liTTle")

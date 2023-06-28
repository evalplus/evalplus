"""
Write a function to toggle the case of all characters in a string.
"""

def toggle_string(string):
 string1 = string.swapcase()
 return string1



assert toggle_string("Python")==("pYTHON")
assert toggle_string("Pangram")==("pANGRAM")
assert toggle_string("LIttLE")==("liTTle")

"""
Write a function to check if a string represents an integer or not.
"""

def check_integer(text):
 assert isinstance(text, str), "invalid inputs" # $_CONTRACT_$
 text = text.strip()
 if len(text) < 1:
    return None
 else:
    if text[0] in '+-':
        text = text[1:]
    return text.isdigit()



assert check_integer("python")==False
assert check_integer("1")==True
assert check_integer("12345")==True

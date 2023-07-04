"""
Write a python function to convert the given string to lower case.
"""

def is_lower(string):
    assert isinstance(string, str), "invalid inputs" # $_CONTRACT_$
    return (string.lower())



assert is_lower("InValid") == "invalid"
assert is_lower("TruE") == "true"
assert is_lower("SenTenCE") == "sentence"

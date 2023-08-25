"""
Write a python function to remove the characters which have odd index values of a given string.
"""

def odd_values_string(str1):
    assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
    return ''.join(str1[i] for i in range(0, len(str1), 2))



assert odd_values_string('abcdef') == 'ace'
assert odd_values_string('python') == 'pto'
assert odd_values_string('data') == 'dt'
assert odd_values_string('lambs') == 'lms'

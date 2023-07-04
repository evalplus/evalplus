"""
Write a python function to remove the characters which have odd index values of a given string.
"""

def odd_values_string(str1):
    assert isinstance(str1, str), "invalid inputs" # $_CONTRACT_$
    result = "" 
    for i in range(len(str1)):
        if i % 2 == 0:
            result = result + str1[i]
    return result



assert odd_values_string('abcdef') == 'ace'
assert odd_values_string('python') == 'pto'
assert odd_values_string('data') == 'dt'
assert odd_values_string('lambs') == 'lms'

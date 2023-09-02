"""
Write a python function to count number of digits in a given string.
"""

def number_ctr(s):
    assert isinstance(s, str), "invalid inputs" # $_CONTRACT_$
    return sum(c.isdigit() for c in s)



assert number_ctr('program2bedone') == 1
assert number_ctr('3wonders') == 1
assert number_ctr('123') == 3
assert number_ctr('3wond-1ers2') == 3

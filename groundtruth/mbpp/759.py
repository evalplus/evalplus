"""
Write a function to check whether a given string is a decimal number with a precision of 2.
"""

def is_decimal(num):
    import re
    dnumre = re.compile(r"""^[0-9]+(\.[0-9]{1,2})?$""")
    result = dnumre.search(num)
    return bool(result)



assert is_decimal('123.11')==True
assert is_decimal('e666.86')==False
assert is_decimal('3.124587')==False
assert is_decimal('1.11')==True
assert is_decimal('1.1.11')==False

"""
Write a function to convert the given decimal number to its binary equivalent, represented as a string with no leading zeros.
"""

def decimal_to_binary(n): 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    return bin(n).replace("0b","") 



assert decimal_to_binary(8) == '1000'
assert decimal_to_binary(18) == '10010'
assert decimal_to_binary(7) == '111'

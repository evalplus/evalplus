"""
Write a python function to check if a given number is one less than twice its reverse.
"""

def check(n):    
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    return n == 2 * int(str(n)[::-1]) - 1



assert check(70) == False
assert check(23) == False
assert check(73) == True

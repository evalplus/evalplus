"""
Write a python function to find the last digit of a given number.
"""

def last_Digit(n) :
    return (n % 10) 



assert last_Digit(123) == 3
assert last_Digit(25) == 5
assert last_Digit(30) == 0

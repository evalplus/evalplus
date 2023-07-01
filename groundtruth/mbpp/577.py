"""
Write a python function to find the last digit in factorial of a given number.
"""

def last_Digit_Factorial(n): 
    assert isinstance(n, (int, float)), "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    if (n == 0): return 1
    elif (n <= 2): return n  
    elif (n == 3): return 6
    elif (n == 4): return 4 
    else: 
      return 0



assert last_Digit_Factorial(4) == 4
assert last_Digit_Factorial(21) == 0
assert last_Digit_Factorial(30) == 0

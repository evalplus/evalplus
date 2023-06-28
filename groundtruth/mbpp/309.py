"""
Write a python function to find the maximum of two numbers.
"""

def maximum(a,b):   
    if a >= b: 
        return a 
    else: 
        return b 



assert maximum(5,10) == 10
assert maximum(-1,-2) == -1
assert maximum(9,7) == 9

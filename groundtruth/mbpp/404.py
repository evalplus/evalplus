"""
Write a python function to find the minimum of two numbers.
"""

def minimum(a,b):   
    if a <= b: 
        return a 
    else: 
        return b 



assert minimum(1,2) == 1
assert minimum(-5,-4) == -5
assert minimum(0,0) == 0

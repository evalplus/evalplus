"""
Write a python function to find quotient of two numbers (rounded down to the nearest integer).
"""

def find(n,m):  
    q = n//m 
    return (q)



assert find(10,3) == 3
assert find(4,2) == 2
assert find(20,5) == 4

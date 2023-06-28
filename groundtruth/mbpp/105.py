"""
Write a python function to count true booleans in the given list.
"""

def count(lst):   
    return sum(lst) 



assert count([True,False,True]) == 2
assert count([False,False]) == 0
assert count([True,True,True]) == 3

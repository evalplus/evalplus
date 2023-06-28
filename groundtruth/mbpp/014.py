"""
Write a python function to find the volume of a triangular prism.
"""

def find_Volume(l,b,h) : 
    return ((l * b * h) / 2) 



assert find_Volume(10,8,6) == 240
assert find_Volume(3,2,2) == 6
assert find_Volume(1,2,1) == 1

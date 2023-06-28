"""
Write a python function to check whether a list of numbers contains only one distinct element or not.
"""

def unique_Element(arr):
    s = set(arr)
    return len(s) == 1



assert unique_Element([1,1,1]) == True
assert unique_Element([1,2,1,2]) == False
assert unique_Element([1,2,3,4,5]) == False

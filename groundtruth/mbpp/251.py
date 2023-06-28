"""
Write a function that takes in a list and an element and inserts the element before each element in the list, and returns the resulting list.
"""

def insert_element(list,element):
 list = [v for elt in list for v in (element, elt)]
 return list



assert insert_element(['Red', 'Green', 'Black'] ,'c')==['c', 'Red', 'c', 'Green', 'c', 'Black']
assert insert_element(['python', 'java'] ,'program')==['program', 'python', 'program', 'java']
assert insert_element(['happy', 'sad'] ,'laugh')==['laugh', 'happy', 'laugh', 'sad']

"""
Write a function that takes in a list and an element and inserts the element before each element in the list, and returns the resulting list.
"""

def insert_element(list1, element):
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    list1 = [v for elt in list1 for v in (element, elt)]
    return list1



assert insert_element(['Red', 'Green', 'Black'] ,'c')==['c', 'Red', 'c', 'Green', 'c', 'Black']
assert insert_element(['python', 'java'] ,'program')==['program', 'python', 'program', 'java']
assert insert_element(['happy', 'sad'] ,'laugh')==['laugh', 'happy', 'laugh', 'sad']

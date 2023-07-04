"""
Write a python function to count the occurence of all elements of list in a tuple.
"""

from collections import Counter 
def count_Occurrence(tup, lst): 
    assert isinstance(tup, tuple), "invalid inputs" # $_CONTRACT_$
    count = 0
    for item in tup: 
        if item in lst: 
            count+= 1 
    return count  



assert count_Occurrence(('a', 'a', 'c', 'b', 'd'),['a', 'b'] ) == 3
assert count_Occurrence((1, 2, 3, 1, 4, 6, 7, 1, 4),[1, 4, 7]) == 6
assert count_Occurrence((1,2,3,4,5,6),[1,2]) == 2

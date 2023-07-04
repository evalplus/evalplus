"""
Write a python function that takes in a tuple and an element and counts the occcurences of the element in the tuple.
"""

def count_X(tup, x): 
    assert isinstance(tup, tuple), "invalid inputs" # $_CONTRACT_$
    count = 0
    for ele in tup: 
        if (ele == x): 
            count = count + 1
    return count 



assert count_X((10, 8, 5, 2, 10, 15, 10, 8, 5, 8, 8, 2),4) == 0
assert count_X((10, 8, 5, 2, 10, 15, 10, 8, 5, 8, 8, 2),10) == 3
assert count_X((10, 8, 5, 2, 10, 15, 10, 8, 5, 8, 8, 2),8) == 4

"""
Write a function to sort each sublist of strings in a given list of lists.
"""

def sort_sublists(list1):
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    assert len(list1) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, list) for x in list1), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, str) for sublist in list1 for x in sublist), "invalid inputs" # $_CONTRACT_$
    return list(map(sorted,list1)) 



assert sort_sublists([['green', 'orange'], ['black', 'white'], ['white', 'black', 'orange']])==[['green', 'orange'], ['black', 'white'], ['black', 'orange', 'white']]
assert sort_sublists([['green', 'orange'], ['black'], ['green', 'orange'], ['white']])==[['green', 'orange'], ['black'], ['green', 'orange'], ['white']]
assert sort_sublists([['a','b'],['d','c'],['g','h'] , ['f','e']])==[['a', 'b'], ['c', 'd'], ['g', 'h'], ['e', 'f']]

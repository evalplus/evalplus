"""
Write a function to extract the nth element from a given list of tuples.
"""

def extract_nth_element(list1, n):
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(tup, tuple) for tup in list1), "invalid inputs" # $_CONTRACT_$
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert all(n < len(tup) for tup in list1), "invalid inputs" # $_CONTRACT_$
    return [x[n] for x in list1]



assert extract_nth_element([('Greyson Fulton', 98, 99), ('Brady Kent', 97, 96), ('Wyatt Knott', 91, 94), ('Beau Turnbull', 94, 98)] ,0)==['Greyson Fulton', 'Brady Kent', 'Wyatt Knott', 'Beau Turnbull']
assert extract_nth_element([('Greyson Fulton', 98, 99), ('Brady Kent', 97, 96), ('Wyatt Knott', 91, 94), ('Beau Turnbull', 94, 98)] ,2)==[99, 96, 94, 98]
assert extract_nth_element([('Greyson Fulton', 98, 99), ('Brady Kent', 97, 96), ('Wyatt Knott', 91, 94), ('Beau Turnbull', 94, 98)],1)==[98, 97, 91, 94]

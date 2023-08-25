"""
Write a function that takes in a dictionary and integer n and filters the dictionary to only include entries with values greater than or equal to n.
"""

def dict_filter(dict1, n):
    assert isinstance(dict1, dict), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, int) for x in dict1.values()), "invalid inputs" # $_CONTRACT_$
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    return {key : value for (key, value) in dict1.items() if value >=n}



assert dict_filter({'Cierra Vega': 175, 'Alden Cantrell': 180, 'Kierra Gentry': 165, 'Pierre Cox': 190},170)=={'Cierra Vega': 175, 'Alden Cantrell': 180, 'Pierre Cox': 190}
assert dict_filter({'Cierra Vega': 175, 'Alden Cantrell': 180, 'Kierra Gentry': 165, 'Pierre Cox': 190},180)=={ 'Alden Cantrell': 180, 'Pierre Cox': 190}
assert dict_filter({'Cierra Vega': 175, 'Alden Cantrell': 180, 'Kierra Gentry': 165, 'Pierre Cox': 190},190)=={ 'Pierre Cox': 190}

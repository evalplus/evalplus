"""
Write a function to check if all values are same in a dictionary.
"""

def check_value(dict1, n):
    assert isinstance(dict1, dict), "invalid inputs" # $_CONTRACT_$
    return all(x == n for x in dict1.values()) 



assert check_value({'Cierra Vega': 12, 'Alden Cantrell': 12, 'Kierra Gentry': 12, 'Pierre Cox': 12},10)==False
assert check_value({'Cierra Vega': 12, 'Alden Cantrell': 12, 'Kierra Gentry': 12, 'Pierre Cox': 12},12)==True
assert check_value({'Cierra Vega': 12, 'Alden Cantrell': 12, 'Kierra Gentry': 12, 'Pierre Cox': 12},5)==False

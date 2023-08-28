"""
Write a function to find the median of three numbers.
"""

def median_numbers(a,b,c):
    assert isinstance(a, (int, float)), "invalid inputs" # $_CONTRACT_$
    assert isinstance(b, (int, float)), "invalid inputs" # $_CONTRACT_$
    assert isinstance(c, (int, float)), "invalid inputs" # $_CONTRACT_$
    return sorted([a,b,c])[1]


assert median_numbers(25,55,65)==55.0
assert median_numbers(20,10,30)==20.0
assert median_numbers(15,45,75)==45.0

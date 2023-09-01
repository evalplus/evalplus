"""
Write a function to find the median length of a trapezium.
"""

def median_trapezium(base1,base2,height):
    assert isinstance(base1, (int, float)), "invalid inputs" # $_CONTRACT_$
    assert isinstance(base2, (int, float)), "invalid inputs" # $_CONTRACT_$
    return (base1 + base2) / 2



assert median_trapezium(15,25,35)==20
assert median_trapezium(10,20,30)==15
assert median_trapezium(6,9,4)==7.5

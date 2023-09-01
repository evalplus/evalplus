"""
Write a python function to find the average of cubes of first n natural numbers.
"""

def find_Average_Of_Cube(n):  
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    return sum([(i ** 3) for i in range(1, n + 1)]) / n



assert find_Average_Of_Cube(2) == 4.5
assert find_Average_Of_Cube(3) == 12
assert find_Average_Of_Cube(1) == 1

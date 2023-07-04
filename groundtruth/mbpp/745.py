"""
Write a function to find numbers within a given range from startnum ti endnum where every number is divisible by every digit it contains. https://www.w3resource.com/python-exercises/lambda/python-lambda-exercise-24.php
"""

def divisible_by_digits(startnum, endnum):
    assert isinstance(startnum, int), "invalid inputs" # $_CONTRACT_$
    assert isinstance(endnum, int), "invalid inputs" # $_CONTRACT_$
    assert startnum <= endnum, "invalid inputs" # $_CONTRACT_$
    return [n for n in range(startnum, endnum+1) \
                if not any(map(lambda x: int(x) == 0 or n%int(x) != 0, str(n)))]



assert divisible_by_digits(1,22)==[1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 15, 22]
assert divisible_by_digits(1,15)==[1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 15]
assert divisible_by_digits(20,25)==[22, 24]

"""
Write a python function to check whether the given number can be represented as sum of non-zero powers of 2 or not.
"""

def is_Sum_Of_Powers_Of_Two(n): 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    return n > 0 and n % 2 == 0



assert is_Sum_Of_Powers_Of_Two(10) == True
assert is_Sum_Of_Powers_Of_Two(7) == False
assert is_Sum_Of_Powers_Of_Two(14) == True

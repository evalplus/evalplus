"""
Write a function to locate the left insertion point for a specified value in sorted order. https://www.w3resource.com/python-exercises/data-structures-and-algorithms/python-data-structure-exercise-24.php
"""

import bisect
def left_insertion(a, x):
    assert isinstance(a, list), "invalid inputs" # $_CONTRACT_$
    assert all(x <= y for x, y in zip(a, a[1:])), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, (int, float)) for x in a), "invalid inputs" # $_CONTRACT_$
    i = bisect.bisect_left(a, x)
    return i



assert left_insertion([1,2,4,5],6)==4
assert left_insertion([1,2,4,5],3)==2
assert left_insertion([1,2,4,5],7)==4

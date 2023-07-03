"""
Write a function to locate the right insertion point for a specified value in sorted order.
"""

import bisect
def right_insertion(a, x):
    assert isinstance(a, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(item, (int, float)) for item in a), "invalid inputs" # $_CONTRACT_$
    assert isinstance(x, (int, float)), "invalid inputs" # $_CONTRACT_$
    return bisect.bisect_right(a, x)



assert right_insertion([1,2,4,5],6)==4
assert right_insertion([1,2,4,5],3)==2
assert right_insertion([1,2,4,5],7)==4

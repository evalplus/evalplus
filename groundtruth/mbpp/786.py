"""
Write a function to locate the right insertion point for a specified value in sorted order.
"""

import bisect
def right_insertion(a, x):
    return bisect.bisect_right(a, x)



assert right_insertion([1,2,4,5],6)==4
assert right_insertion([1,2,4,5],3)==2
assert right_insertion([1,2,4,5],7)==4

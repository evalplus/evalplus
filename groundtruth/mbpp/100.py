"""
Write a function to find the next smallest palindrome of a specified integer, returned as an integer.
"""

import sys
def next_smallest_palindrome(num):
    assert isinstance(num, int), "invalid inputs" # $_CONTRACT_$
    assert num >= 0, "invalid inputs" # $_CONTRACT_$
    numstr = str(num)
    for i in range(num+1,sys.maxsize):
        if str(i) == str(i)[::-1]:
            return i



assert next_smallest_palindrome(99)==101
assert next_smallest_palindrome(1221)==1331
assert next_smallest_palindrome(120)==121

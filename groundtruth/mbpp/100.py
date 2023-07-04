"""
Write a function to find the next smallest palindrome of a specified integer, returned as an integer.
"""

def next_smallest_palindrome(num):
    assert isinstance(num, int), "invalid inputs" # $_CONTRACT_$
    assert num >= 0, "invalid inputs" # $_CONTRACT_$
    ret = num + 1
    while not str(ret) == str(ret)[::-1]:
        ret += 1
    return ret



assert next_smallest_palindrome(99)==101
assert next_smallest_palindrome(1221)==1331
assert next_smallest_palindrome(120)==121

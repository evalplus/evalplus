"""
Write a function to find the next smallest palindrome of a specified integer, returned as an integer.
"""

def next_smallest_palindrome(num):
    assert isinstance(num, int), "invalid inputs" # $_CONTRACT_$
    assert num >= 0, "invalid inputs" # $_CONTRACT_$
    if all(digit == '9' for digit in str(num)):
        return num + 2
    else:
        num = [int(digit) for digit in str(num)]
        n = len(num)
        mid = n // 2
        left_smaller = False
        # if n is odd, ignore the middle digit at first
        i = mid - 1
        j = mid + 1 if n % 2 else mid
        while i >= 0 and num[i] == num[j]:
            i -= 1
            j += 1
        # stop if traverse end or difference found
        if i < 0 or num[i] < num[j]:
            left_smaller = True
        # copy left to right
        while i >= 0:
            num[j] = num[i]
            j += 1
            i -= 1
        # the middle digit must be incremented
        if left_smaller:
            carry = 1
            i = mid - 1
            if n % 2:
                num[mid] += carry
                carry = num[mid] // 10
                num[mid] %= 10
                j = mid + 1
            else:
                j = mid
            while i >= 0:
                num[i] += carry
                carry = num[i] // 10
                num[i] %= 10
                num[j] = num[i]
                j += 1
                i -= 1
    return int("".join(map(str, num)))



assert next_smallest_palindrome(99)==101
assert next_smallest_palindrome(1221)==1331
assert next_smallest_palindrome(120)==121

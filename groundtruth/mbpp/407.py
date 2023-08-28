"""
Write a function to create the next bigger number by rearranging the digits of a given number, return None if not possible.
"""

def rearrange_bigger(n):
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    digits = list(str(n))
    for i in range(len(digits) - 1, 0, -1):
        if digits[i] > digits[i-1]:
            digits[i], digits[i-1] = digits[i-1], digits[i]
            return int("".join(digits))
    return None




assert rearrange_bigger(12)==21
assert rearrange_bigger(10)==None
assert rearrange_bigger(102)==120

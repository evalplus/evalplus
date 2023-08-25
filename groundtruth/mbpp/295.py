"""
Write a function to return the sum of all divisors of a number.
"""

def sum_div(number):
    assert isinstance(number, int) and number > 0, "invalid inputs" # $_CONTRACT_$
    res = 1
    i = 2
    while i * i <= number:
        if number % i == 0:
            res += i
            if i * i != number:
                res += number / i
        i += 1
    return res


assert sum_div(8)==7
assert sum_div(12)==16
assert sum_div(7)==1

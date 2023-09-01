"""
Write a function to check whether the given number is armstrong or not.
"""

def armstrong_number(number):
    assert isinstance(number, int), "invalid inputs" # $_CONTRACT_$
    assert number > 0, "invalid inputs" # $_CONTRACT_$
    order = len(str(number))
    return sum([int(i) ** order for i in str(number)]) == number



assert armstrong_number(153)==True
assert armstrong_number(259)==False
assert armstrong_number(4458)==False

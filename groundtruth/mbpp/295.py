"""
Write a function to return the sum of all divisors of a number.
"""

def sum_div(number):
    assert isinstance(number, int) and number > 0, "invalid inputs" # $_CONTRACT_$
    divisors = [1]
    for i in range(2, number):
        if (number % i)==0:
            divisors.append(i)
    return sum(divisors)



assert sum_div(8)==7
assert sum_div(12)==16
assert sum_div(7)==1

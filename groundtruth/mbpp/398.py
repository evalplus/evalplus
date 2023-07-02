"""
Write a function to compute the sum of digits of each number of a given list.
"""

def sum_of_digits(nums):
    assert isinstance(nums, list), "invalid inputs" # $_CONTRACT_$
    return sum(int(el) for n in nums for el in str(n) if el.isdigit())



assert sum_of_digits([10,2,56])==14
assert sum_of_digits([[10,20,4,5,'b',70,'a']])==19
assert sum_of_digits([10,20,-4,5,-70])==19

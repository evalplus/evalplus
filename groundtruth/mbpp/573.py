"""
Write a python function to calculate the product of the unique numbers in a given list.
"""

def unique_product(list_data):
    assert isinstance(list_data, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, (int, float)) for x in list_data), "invalid inputs" # $_CONTRACT_$
    from functools import reduce
    return reduce(lambda x, y: x*y, set(list_data))



assert unique_product([10, 20, 30, 40, 20, 50, 60, 40]) ==  720000000
assert unique_product([1, 2, 3, 1,]) == 6
assert unique_product([7, 8, 9, 0, 1, 1]) == 0

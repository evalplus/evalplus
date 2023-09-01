"""
Write a python function to find the product of the array multiplication modulo n.
"""

def find_remainder(arr, n): 
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert len(arr) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, (int, float)) for x in arr), "invalid inputs" # $_CONTRACT_$
    assert isinstance(n, (int, float)), "invalid inputs" # $_CONTRACT_$
    from functools import reduce
    return reduce(lambda x, y: x * y, arr) % n



assert find_remainder([ 100, 10, 5, 25, 35, 14 ],11) ==9
assert find_remainder([1,1,1],1) == 0
assert find_remainder([1,2,1],2) == 0

"""
Write a python function which takes a list of integers and only returns the odd ones.
"""

def Split(l): 
    assert isinstance(l, list), "invalid inputs" # $_CONTRACT_$
    assert len(l) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, int) for x in l), "invalid inputs" # $_CONTRACT_$
    return list(filter(lambda x: x % 2 == 1, l))



assert Split([1,2,3,4,5,6]) == [1,3,5]
assert Split([10,11,12,13]) == [11,13]
assert Split([7,8,9,1]) == [7,9,1]

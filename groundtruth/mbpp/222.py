"""
Write a function to check if all the elements in tuple have same data type or not.
"""

def check_type(test_tuple):
    assert isinstance(test_tuple, tuple), "invalid inputs" # $_CONTRACT_$
    assert len(test_tuple) > 0, "invalid inputs" # $_CONTRACT_$
    res = True
    for ele in test_tuple:
        if not isinstance(ele, type(test_tuple[0])):
            res = False
            break
    return (res) 



assert check_type((5, 6, 7, 3, 5, 6) ) == True
assert check_type((1, 2, "4") ) == False
assert check_type((3, 2, 1, 4, 5) ) == True

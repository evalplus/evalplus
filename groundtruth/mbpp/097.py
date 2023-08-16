"""
Write a function to find frequency of each element in a flattened list of lists, returned in a dictionary.
"""

def frequency_lists(list1):
    def is_hashable(obj): # $_CONTRACT_$
        try: # $_CONTRACT_$
            hash(obj) # $_CONTRACT_$
            return True # $_CONTRACT_$
        except TypeError: # $_CONTRACT_$
            return False # $_CONTRACT_$
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    assert len(list1) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(item, list) for item in list1), "invalid inputs" # $_CONTRACT_$
    assert all(is_hashable(item) for sublist in list1 for item in sublist), "invalid inputs" # $_CONTRACT_$
    list1 = [item for sublist in list1 for item in sublist]
    return {x: list1.count(x) for x in list1}




assert frequency_lists([[1, 2, 3, 2], [4, 5, 6, 2], [7, 8, 9, 5]])=={1: 1, 2: 3, 3: 1, 4: 1, 5: 2, 6: 1, 7: 1, 8: 1, 9: 1}
assert frequency_lists([[1,2,3,4],[5,6,7,8],[9,10,11,12]])=={1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1,10:1,11:1,12:1}
assert frequency_lists([[20,30,40,17],[18,16,14,13],[10,20,30,40]])=={20:2,30:2,40:2,17: 1,18:1, 16: 1,14: 1,13: 1, 10: 1}

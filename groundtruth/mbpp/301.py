"""
Write a function to find the depth of a dictionary.
"""

def dict_depth_aux(d):
    if isinstance(d, dict):
        return 1 + (max(map(dict_depth_aux, d.values())) if d else 0)
    return 0


def dict_depth(d):
    assert isinstance(d, dict), "invalid inputs" # $_CONTRACT_$
    return dict_depth_aux(d)


assert dict_depth({'a':1, 'b': {'c': {'d': {}}}})==4
assert dict_depth({'a':1, 'b': {'c':'python'}})==2
assert dict_depth({1: 'Sun', 2: {3: {4:'Mon'}}})==3

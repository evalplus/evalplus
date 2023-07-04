"""
Write a function to reverse each string in a given list of string values.
"""

def reverse_string_list(stringlist):
    assert isinstance(stringlist, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, str) for x in stringlist), "invalid inputs" # $_CONTRACT_$
    result = [x[::-1] for x in stringlist]
    return result



assert reverse_string_list(['Red', 'Green', 'Blue', 'White', 'Black'])==['deR', 'neerG', 'eulB', 'etihW', 'kcalB']
assert reverse_string_list(['john','amal','joel','george'])==['nhoj','lama','leoj','egroeg']
assert reverse_string_list(['jack','john','mary'])==['kcaj','nhoj','yram']

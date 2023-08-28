"""
Write a function to find the minimum value in a given heterogeneous list.
"""

def min_val(listval):
     assert isinstance(listval, list), "invalid inputs" # $_CONTRACT_$
     assert len(listval) > 0, "invalid inputs" # $_CONTRACT_$
     assert any(isinstance(i, int) for i in listval), "invalid inputs" # $_CONTRACT_$
     min_val = min(i for i in listval if isinstance(i, int))
     return min_val



assert min_val(['Python', 3, 2, 4, 5, 'version'])==2
assert min_val(['Python', 15, 20, 25])==15
assert min_val(['Python', 30, 20, 40, 50, 'version'])==20

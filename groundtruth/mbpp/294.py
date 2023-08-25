"""
Write a function to find the maximum value in a given heterogeneous list.
"""

def max_val(listval):
     assert isinstance(listval, list), "invalid inputs" # $_CONTRACT_$
     assert len(listval) > 0, "invalid inputs" # $_CONTRACT_$
     assert any(isinstance(i, int) for i in listval), "invalid inputs" # $_CONTRACT_$
     max_val = max(i for i in listval if isinstance(i, int)) 
     return max_val



assert max_val(['Python', 3, 2, 4, 5, 'version'])==5
assert max_val(['Python', 15, 20, 25])==25
assert max_val(['Python', 30, 20, 40, 50, 'version'])==50

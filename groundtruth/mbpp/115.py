"""
Write a function to check whether all dictionaries in a list are empty or not.
"""

def empty_dit(list1):
 assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
 return all(len(d) == 0 for d in list1 if isinstance(d, dict))



assert empty_dit([{},{},{}])==True
assert empty_dit([{1,2},{},{}])==True
assert empty_dit([{}])==True

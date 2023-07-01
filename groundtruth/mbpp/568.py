"""
Write a function to create a list of N empty dictionaries.
"""

def empty_list(length):
 assert isinstance(length, int), "invalid inputs" # $_CONTRACT_$
 empty_list = [{} for _ in range(length)]
 return empty_list



assert empty_list(5)==[{},{},{},{},{}]
assert empty_list(6)==[{},{},{},{},{},{}]
assert empty_list(7)==[{},{},{},{},{},{},{}]

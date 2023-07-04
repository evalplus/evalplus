"""
Write a function to extract specified size of strings from a given list of string values.
"""

def extract_string(str1, l):
    assert isinstance(str1, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(ele, str) for ele in str1), "invalid inputs" # $_CONTRACT_$
    assert isinstance(l, int), "invalid inputs" # $_CONTRACT_$
    result = [e for e in str1 if len(e) == l] 
    return result



assert extract_string(['Python', 'list', 'exercises', 'practice', 'solution'] ,8)==['practice', 'solution']
assert extract_string(['Python', 'list', 'exercises', 'practice', 'solution'] ,6)==['Python']
assert extract_string(['Python', 'list', 'exercises', 'practice', 'solution'] ,9)==['exercises']

"""
Given a list of tuples, write a function that returns the first value of the tuple with the smallest second value.
"""

from operator import itemgetter 
def index_minimum(test_list):
  assert isinstance(test_list, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(item, tuple) and len(item) >= 2 for item in test_list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(item[1], (int, float)) for item in test_list), "invalid inputs" # $_CONTRACT_$
  res = min(test_list, key = itemgetter(1))[0]
  return (res) 



assert index_minimum([('Rash', 143), ('Manjeet', 200), ('Varsha', 100)]) == 'Varsha'
assert index_minimum([('Yash', 185), ('Dawood', 125), ('Sanya', 175)]) == 'Dawood'
assert index_minimum([('Sai', 345), ('Salman', 145), ('Ayesha', 96)]) == 'Ayesha'

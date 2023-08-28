"""
Write a function to get a copy of a tuple, and append n to the list item at the index of m in the copied tuple.
"""

from copy import deepcopy
def colon_tuplex(tuplex,m,n):
  assert isinstance(tuplex, tuple), "invalid inputs" # $_CONTRACT_$
  assert isinstance(m, int), "invalid inputs" # $_CONTRACT_$
  assert 0 <= m < len(tuplex), "invalid inputs" # $_CONTRACT_$
  assert isinstance(tuplex[m], list), "invalid inputs" # $_CONTRACT_$
  tuplex_colon = deepcopy(tuplex)
  tuplex_colon[m].append(n)
  return tuplex_colon



assert colon_tuplex(("HELLO", 5, [], True) ,2,50)==("HELLO", 5, [50], True)
assert colon_tuplex(("HELLO", 5, [], True) ,2,100)==(("HELLO", 5, [100],True))
assert colon_tuplex(("HELLO", 5, [], True) ,2,500)==("HELLO", 5, [500], True)

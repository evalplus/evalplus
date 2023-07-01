"""
Write a function to find the n most expensive items in a given dataset.
"""

import heapq
def expensive_items(items,n):
  assert isinstance(items, list), "invalid inputs" # $_CONTRACT_$
  assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
  assert n >= 0, "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, dict) for x in items), "invalid inputs" # $_CONTRACT_$
  assert all('name' in x.keys() for x in items), "invalid inputs" # $_CONTRACT_$
  assert all('price' in x.keys() for x in items), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x['price'], (int, float)) for x in items), "invalid inputs" # $_CONTRACT_$
  expensive_items = heapq.nlargest(n, items, key=lambda s: s['price'])
  return expensive_items



assert expensive_items([{'name': 'Item-1', 'price': 101.1},{'name': 'Item-2', 'price': 555.22}],1)==[{'name': 'Item-2', 'price': 555.22}]
assert expensive_items([{'name': 'Item-1', 'price': 101.1},{'name': 'Item-2', 'price': 555.22}, {'name': 'Item-3', 'price': 45.09}],2)==[{'name': 'Item-2', 'price': 555.22},{'name': 'Item-1', 'price': 101.1}]
assert expensive_items([{'name': 'Item-1', 'price': 101.1},{'name': 'Item-2', 'price': 555.22}, {'name': 'Item-3', 'price': 45.09},{'name': 'Item-4', 'price': 22.75}],1)==[{'name': 'Item-2', 'price': 555.22}]

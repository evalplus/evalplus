"""
Write a function to sort a dictionary by value.
"""

from collections import Counter
def sort_counter(dict1):
 assert isinstance(dict1, dict), "invalid inputs" # $_CONTRACT_$
 assert all(isinstance(x, (int, float)) for x in dict1.values()), "invalid inputs" # $_CONTRACT_$
 x = Counter(dict1)
 sort_counter=x.most_common()
 return sort_counter



assert sort_counter({'Math':81, 'Physics':83, 'Chemistry':87})==[('Chemistry', 87), ('Physics', 83), ('Math', 81)]
assert sort_counter({'Math':400, 'Physics':300, 'Chemistry':250})==[('Math', 400), ('Physics', 300), ('Chemistry', 250)]
assert sort_counter({'Math':900, 'Physics':1000, 'Chemistry':1250})==[('Chemistry', 1250), ('Physics', 1000), ('Math', 900)]

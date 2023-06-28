"""
Write a function that takes two lists and returns true if they have at least one common element.
"""

def common_element(list1, list2):
     result = False
     for x in list1:
         for y in list2:
             if x == y:
                 result = True
                 return result



assert common_element([1,2,3,4,5], [5,6,7,8,9])==True
assert common_element([1,2,3,4,5], [6,7,8,9])==None
assert common_element(['a','b','c'], ['d','b','e'])==True

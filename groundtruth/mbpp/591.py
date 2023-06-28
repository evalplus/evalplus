"""
Write a python function to interchange the first and last elements in a list.
"""

def swap_List(newList): 
    size = len(newList) 
    temp = newList[0] 
    newList[0] = newList[size - 1] 
    newList[size - 1] = temp  
    return newList 



assert swap_List([12, 35, 9, 56, 24]) == [24, 35, 9, 56, 12]
assert swap_List([1, 2, 3]) == [3, 2, 1]
assert swap_List([4, 5, 6]) == [6, 5, 4]

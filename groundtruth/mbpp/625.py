"""
Write a python function to interchange the first and last element in a given list.
"""

def swap_List(newList): 
    size = len(newList) 
    temp = newList[0] 
    newList[0] = newList[size - 1] 
    newList[size - 1] = temp   
    return newList 



assert swap_List([1,2,3]) == [3,2,1]
assert swap_List([1,2,3,4,4]) == [4,2,3,4,1]
assert swap_List([4,5,6]) == [6,5,4]

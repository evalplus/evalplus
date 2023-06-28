"""
Write a python function to find the smallest missing number from a sorted list of natural numbers.
"""

def find_First_Missing(array,start=0,end=None):
    if end is None:
      end = len(array) - 1   
    if (start > end): 
        return end + 1
    if (start != array[start]): 
        return start; 
    mid = int((start + end) / 2) 
    if (array[mid] == mid): 
        return find_First_Missing(array,mid+1,end) 
    return find_First_Missing(array,start,mid) 



assert find_First_Missing([0,1,2,3]) == 4
assert find_First_Missing([0,1,2,6,9]) == 3
assert find_First_Missing([2,3,5,8,9]) == 0

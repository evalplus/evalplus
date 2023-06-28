"""
Write a python function to find the sum of an array.
"""

def _sum(arr):  
    sum=0
    for i in arr: 
        sum = sum + i      
    return(sum)  



assert _sum([1, 2, 3]) == 6
assert _sum([15, 12, 13, 10]) == 50
assert _sum([0, 1, 2]) == 3

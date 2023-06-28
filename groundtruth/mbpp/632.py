"""
Write a python function to move all zeroes to the end of the given list.
"""

def move_zero(num_list):
    a = [0 for i in range(num_list.count(0))]
    x = [i for i in num_list if i != 0]
    return x + a



assert move_zero([1,0,2,0,3,4]) == [1,2,3,4,0,0]
assert move_zero([2,3,2,0,0,4,0,5,0]) == [2,3,2,4,5,0,0,0,0]
assert move_zero([0,1,0,1,1]) == [1,1,1,0,0]

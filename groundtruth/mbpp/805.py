"""
Write a function that returns the list in a list of lists whose sum of elements is the highest.
"""

def max_sum_list(lists):
 return max(lists, key=sum)



assert max_sum_list([[1,2,3], [4,5,6], [10,11,12], [7,8,9]])==[10, 11, 12]
assert max_sum_list([[3,2,1], [6,5,4], [12,11,10]])==[12,11,10]
assert max_sum_list([[2,3,1]])==[2,3,1]

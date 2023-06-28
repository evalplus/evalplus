"""
Write a function that takes in a list and an integer n and returns a list containing the n largest items from the list.
"""

import heapq
def larg_nnum(list1,n):
 largest=heapq.nlargest(n,list1)
 return largest



assert set(larg_nnum([10, 20, 50, 70, 90, 20, 50, 40, 60, 80, 100],2))==set([100,90])
assert set(larg_nnum([10, 20, 50, 70, 90, 20, 50, 40, 60, 80, 100],5))==set([100,90,80,70,60])
assert set(larg_nnum([10, 20, 50, 70, 90, 20, 50, 40, 60, 80, 100],3))==set([100,90,80])

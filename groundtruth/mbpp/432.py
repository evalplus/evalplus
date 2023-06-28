"""
Write a function to find the median length of a trapezium.
"""

def median_trapezium(base1,base2,height):
 median = 0.5 * (base1+ base2)
 return median



assert median_trapezium(15,25,35)==20
assert median_trapezium(10,20,30)==15
assert median_trapezium(6,9,4)==7.5

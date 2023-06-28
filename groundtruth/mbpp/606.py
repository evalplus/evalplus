"""
Write a function to convert degrees to radians.
"""

import math
def radian_degree(degree):
 radian = degree*(math.pi/180)
 return radian



assert radian_degree(90)==1.5707963267948966
assert radian_degree(60)==1.0471975511965976
assert radian_degree(120)==2.0943951023931953

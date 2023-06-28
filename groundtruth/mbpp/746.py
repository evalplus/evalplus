"""
Write a function to find area of a sector. The function takes the radius and angle as inputs. Function should return None if the angle is larger than 360 degrees.
"""

import math
def sector_area(r,a):
    if a > 360:
        return None
    return (math.pi*r**2) * (a/360)



assert sector_area(4,45)==6.283185307179586
assert sector_area(9,45)==31.808625617596654
assert sector_area(9,361)==None

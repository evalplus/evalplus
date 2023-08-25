"""
Write a function to get the angle of a complex number.
"""

import cmath
def angle_complex(a,b):
  assert isinstance(a, (int, float)) or isinstance(a, float), "invalid inputs" # $_CONTRACT_$
  assert isinstance(b, complex) or isinstance(b, float), "invalid inputs" # $_CONTRACT_$
  assert b.real == 0, "invalid inputs" # $_CONTRACT_$
  angle=cmath.phase(a+b)
  return angle

import math

assert math.isclose(angle_complex(0,1j), 1.5707963267948966, rel_tol=0.001)
assert math.isclose(angle_complex(2,1j), 0.4636476090008061, rel_tol=0.001)
assert math.isclose(angle_complex(0,2j), 1.5707963267948966, rel_tol=0.001)

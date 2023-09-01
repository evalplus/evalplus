"""
Write a function to find the directrix of a parabola.
"""

def parabola_directrix(a, b, c): 
  assert isinstance(a, (int, float)), "invalid inputs" # $_CONTRACT_$
  assert isinstance(b, (int, float)), "invalid inputs" # $_CONTRACT_$
  assert isinstance(c, (int, float)), "invalid inputs" # $_CONTRACT_$
  return ((int)(c - ((b * b) + 1) * 4 * a ))



assert parabola_directrix(5,3,2)==-198
assert parabola_directrix(9,8,4)==-2336
assert parabola_directrix(2,4,6)==-130

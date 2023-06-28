"""
Write a function to calculate the sum (n - 2*i) from i=0 to n // 2, for instance n + (n-2) + (n-4)... (until n-x =< 0).
"""

def sum_series(n):
  if n < 1:
    return 0
  else:
    return n + sum_series(n - 2)



assert sum_series(6) == 12
assert sum_series(10) == 30
assert sum_series(9) == 25

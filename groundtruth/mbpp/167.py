"""
Write a python function to find the smallest power of 2 greater than or equal to n.
"""

def next_power_of_2(n): 
  assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
  assert n >= 0, "invalid inputs" # $_CONTRACT_$
  if n and not n & (n - 1):
    return n

  count = 0
  while n != 0: 
    n >>= 1
    count += 1

  return 1 << count; 



assert next_power_of_2(0) == 1
assert next_power_of_2(5) == 8
assert next_power_of_2(17) == 32

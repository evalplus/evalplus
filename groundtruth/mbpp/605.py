"""
Write a function to check if the given integer is a prime number.
"""

import math
def prime_num(num):
  assert isinstance(num, int), "invalid inputs" # $_CONTRACT_$
  if num <= 1:
    return False
  for i in range(2, int(math.sqrt(num)) + 1):
    if num % i == 0:
      return False
  return True



assert prime_num(13)==True
assert prime_num(7)==True
assert prime_num(-1010)==False

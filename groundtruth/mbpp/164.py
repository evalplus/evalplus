"""
Write a function to determine if the sum of the divisors of two integers are the same.
"""

import math 
def div_sum(n): 
  assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
  assert n > 0, "invalid inputs" # $_CONTRACT_$
  total = 1
  i = 2

  while i * i <= n:
    if (n % i == 0):
      total = (total + i + math.floor(n / i))
    i += 1

  return total

def are_equivalent(num1, num2): 
    return div_sum(num1) == div_sum(num2); 



assert are_equivalent(36, 57) == False
assert are_equivalent(2, 4) == False
assert are_equivalent(23, 47) == True

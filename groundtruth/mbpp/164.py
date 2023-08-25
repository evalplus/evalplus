"""
Write a function to determine if the sum of the divisors of two integers are the same.
"""

import math 
def div_sum(n): 
  total = 1
  i = 2
  while i * i <= n:
    if (n % i == 0):
      total = total + i + n / i
    i += 1
  return total

def are_equivalent(num1, num2): 
  assert isinstance(num1, int), "invalid inputs" # $_CONTRACT_$
  assert isinstance(num2, int), "invalid inputs" # $_CONTRACT_$
  assert num1 > 0, "invalid inputs" # $_CONTRACT_$
  assert num2 > 0, "invalid inputs" # $_CONTRACT_$
  return div_sum(num1) == div_sum(num2); 



assert are_equivalent(36, 57) == False
assert are_equivalent(2, 4) == False
assert are_equivalent(23, 47) == True

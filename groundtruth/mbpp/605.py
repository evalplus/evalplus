"""
Write a function to check if the given integer is a prime number.
"""

def prime_num(num):
  assert isinstance(num, int), "invalid inputs" # $_CONTRACT_$
  assert num >= 0, "invalid inputs" # $_CONTRACT_$
  if num >=1:
   for i in range(2, num//2):
     if (num % i) == 0:
                return False
     else:
                return True
  else:
          return False



assert prime_num(13)==True
assert prime_num(7)==True
assert prime_num(-1010)==False

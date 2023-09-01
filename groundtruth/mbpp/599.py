"""
Write a function to find sum and average of first n natural numbers.
"""

def sum_average(number):
   assert isinstance(number, int), "invalid inputs" # $_CONTRACT_$
   assert number > 0, "invalid inputs" # $_CONTRACT_$
   sum_ = sum(range(1, number+1))
   average = sum_/number
   return sum_, average



assert sum_average(10)==(55, 5.5)
assert sum_average(15)==(120, 8.0)
assert sum_average(20)==(210, 10.5)

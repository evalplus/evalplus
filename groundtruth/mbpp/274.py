"""
Write a python function that takes in a positive integer n and finds the sum of even index binomial coefficients.
"""

import math  
def even_binomial_Coeff_Sum( n): 
    return (1 << (n - 1)) 



assert even_binomial_Coeff_Sum(4) == 8
assert even_binomial_Coeff_Sum(6) == 32
assert even_binomial_Coeff_Sum(2) == 2

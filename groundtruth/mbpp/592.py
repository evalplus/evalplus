"""
Write a python function to find the sum of the product of consecutive binomial co-efficients.
"""

def binomial_Coeff(n, k): 
    C = [0] * (k + 1); 
    C[0] = 1; # nC0 is 1 
    for i in range(1,n + 1):  
        for j in range(min(i, k),0,-1): 
            C[j] = C[j] + C[j - 1]; 
    return C[k]; 

def sum_Of_product(n): 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    return binomial_Coeff(2 * n, n - 1); 



assert sum_Of_product(3) == 15
assert sum_Of_product(4) == 56
assert sum_Of_product(1) == 1

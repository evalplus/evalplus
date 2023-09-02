"""
Write a python function to find the sum of fourth power of first n odd natural numbers.
"""

def odd_num_sum(n) : 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n >= 1, "invalid inputs" # $_CONTRACT_$
    j = 0
    sm = 0
    for i in range(1,n + 1) : 
        j = (2*i-1) 
        sm = sm + (j*j*j*j)   
    return sm 



assert odd_num_sum(2) == 82
assert odd_num_sum(3) == 707
assert odd_num_sum(4) == 3108

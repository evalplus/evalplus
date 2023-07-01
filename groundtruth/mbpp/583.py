"""
Write a function which returns nth catalan number.
"""

def catalan_number(num):
    assert isinstance(num, int), "invalid inputs" # $_CONTRACT_$
    assert num >= 0, "invalid inputs" # $_CONTRACT_$
    if num <=1:
         return 1   
    res_num = 0
    for i in range(num):
        res_num += catalan_number(i) * catalan_number(num-i-1)
    return res_num



assert catalan_number(10)==16796
assert catalan_number(9)==4862
assert catalan_number(7)==429

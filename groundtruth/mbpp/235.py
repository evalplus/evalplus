"""
Write a python function to set all even bits of a given number.
"""

def even_bit_set_number(n): 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    count = 0;res = 0;temp = n 
    while(temp > 0): 
        if (count % 2 == 1): 
            res |= (1 << count)
        count+=1
        temp >>= 1
    return (n | res) 



assert even_bit_set_number(10) == 10
assert even_bit_set_number(20) == 30
assert even_bit_set_number(30) == 30

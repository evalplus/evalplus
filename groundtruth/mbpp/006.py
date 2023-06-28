"""
Write a python function to check whether the two numbers differ at one bit position only or not.
"""

def is_Power_Of_Two(x): 
    return x and (not(x & (x - 1))) 
def differ_At_One_Bit_Pos(a: int,b: int):
    assert isinstance(a, int), "invalid inputs" # $_CONTRACT_$
    assert isinstance(b, int), "invalid inputs" # $_CONTRACT_$ 
    return is_Power_Of_Two(a ^ b)



assert differ_At_One_Bit_Pos(13,9) == True
assert differ_At_One_Bit_Pos(15,8) == False
assert differ_At_One_Bit_Pos(2,4) == False
assert differ_At_One_Bit_Pos(2, 3) == True
assert differ_At_One_Bit_Pos(5, 1) == True
assert differ_At_One_Bit_Pos(1, 5) == True

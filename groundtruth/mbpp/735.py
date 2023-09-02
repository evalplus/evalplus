"""
Write a python function to toggle bits of the number except the first and the last bit. https://www.geeksforgeeks.org/toggle-bits-number-expect-first-last-bits/
"""

def toggle_middle_bits(n): 
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    binary = bin(n)[2:]
    toggled = ''.join(['0' if i == '1' else '1' for i in binary[1:-1]])
    return int(binary[0] + toggled + binary[-1], 2)



assert toggle_middle_bits(9) == 15
assert toggle_middle_bits(10) == 12
assert toggle_middle_bits(11) == 13
assert toggle_middle_bits(0b1000001) == 0b1111111
assert toggle_middle_bits(0b1001101) == 0b1110011

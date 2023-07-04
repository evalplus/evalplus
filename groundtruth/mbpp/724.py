"""
Write a function that takes base and power as arguments and calculate the sum of all digits of the base to the specified power.
"""

def power_base_sum(base, power):
    assert isinstance(base, int), "invalid inputs" # $_CONTRACT_$
    assert isinstance(power, int), "invalid inputs" # $_CONTRACT_$
    return sum([int(i) for i in str(pow(base, power))])



assert power_base_sum(2,100)==115
assert power_base_sum(8,10)==37
assert power_base_sum(8,15)==62
assert power_base_sum(3,3)==9

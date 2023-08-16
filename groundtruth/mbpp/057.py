"""
Write a python function to find the largest number that can be formed with the given list of digits.
"""

def find_Max_Num(arr) : 
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(item, int) and 0 <= item <= 9 for item in arr), "invalid inputs" # $_CONTRACT_$
    arr.sort(reverse = True)
    return int("".join(map(str,arr)))



assert find_Max_Num([1,2,3]) == 321
assert find_Max_Num([4,5,6,1]) == 6541
assert find_Max_Num([1,2,3,9]) == 9321

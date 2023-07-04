"""
Write a python function to find the largest number that can be formed with the given list of digits.
"""

def find_Max_Num(arr) : 
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(item, int) and 0 <= item <= 9 for item in arr), "invalid inputs" # $_CONTRACT_$
    n = len(arr)
    arr.sort(reverse = True) 
    num = arr[0] 
    for i in range(1,n) : 
        num = num * 10 + arr[i] 
    return num 



assert find_Max_Num([1,2,3]) == 321
assert find_Max_Num([4,5,6,1]) == 6541
assert find_Max_Num([1,2,3,9]) == 9321

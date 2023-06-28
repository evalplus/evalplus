"""
Write a python function to count the number of pairs whose sum is equal to ‘sum’. The funtion gets as input a list of numbers and the sum,
"""

def get_pairs_count(arr, sum):
    count = 0  
    for i in range(len(arr)):
        for j in range(i + 1,len(arr)):
            if arr[i] + arr[j] == sum:
                count += 1
    return count



assert get_pairs_count([1,1,1,1],2) == 6
assert get_pairs_count([1,5,7,-1,5],6) == 3
assert get_pairs_count([1,-2,3],1) == 1
assert get_pairs_count([-1,-2,3],-3) == 1

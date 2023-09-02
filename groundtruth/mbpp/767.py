"""
Write a python function to count the number of pairs whose sum is equal to ‘sum’. The funtion gets as input a list of numbers and the sum,
"""

def get_pairs_count(arr, sum_):
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, (int, float)) for x in arr), "invalid inputs" # $_CONTRACT_$
    assert isinstance(sum_, (int, float)), "invalid inputs" # $_CONTRACT_$
    cnt = 0
    for n in arr:
        cnt += arr.count(sum_ - n)
        if sum_ - n == n:
            cnt -= 1
    return cnt / 2



assert get_pairs_count([1,1,1,1],2) == 6
assert get_pairs_count([1,5,7,-1,5],6) == 3
assert get_pairs_count([1,-2,3],1) == 1
assert get_pairs_count([-1,-2,3],-3) == 1

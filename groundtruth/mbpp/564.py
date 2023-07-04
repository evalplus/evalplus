"""
Write a python function which takes a list of integers and counts the number of possible unordered pairs where both elements are unequal.
"""

def count_Pairs(arr,n): 
    assert isinstance(arr, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, int) for x in arr), "invalid inputs" # $_CONTRACT_$
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n <= len(arr), "invalid inputs" # $_CONTRACT_$
    cnt = 0; 
    for i in range(n): 
        for j in range(i + 1,n): 
            if (arr[i] != arr[j]): 
                cnt += 1; 
    return cnt; 



assert count_Pairs([1,2,1],3) == 2
assert count_Pairs([1,1,1,1],4) == 0
assert count_Pairs([1,2,3,4,5],5) == 10

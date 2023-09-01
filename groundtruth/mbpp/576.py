"""
Write a python function to check whether a list is sublist of another or not.
"""

def is_Sub_Array(A,B): 
    assert isinstance(A, list), "invalid inputs" # $_CONTRACT_$
    assert isinstance(B, list), "invalid inputs" # $_CONTRACT_$
    a = 0
    b = 0
    while a < len(A) and b < len(B):
        if A[a] == B[b]:
            a += 1
            b += 1
        else:
            a += 1
    return b == len(B)




assert is_Sub_Array([1,4,3,5],[1,2]) == False
assert is_Sub_Array([1,2,1],[1,2,1]) == True
assert is_Sub_Array([1,0,2,2],[2,2,0]) ==False

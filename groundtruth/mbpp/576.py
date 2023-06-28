"""
Write a python function to check whether a list is sublist of another or not.
"""

def is_Sub_Array(A,B): 
    n = len(A)
    m = len(B)
    i = 0; j = 0; 
    while (i < n and j < m):  
        if (A[i] == B[j]): 
            i += 1; 
            j += 1; 
            if (j == m): 
                return True;  
        else: 
            i = i - j + 1; 
            j = 0;       
    return False; 



assert is_Sub_Array([1,4,3,5],[1,2]) == False
assert is_Sub_Array([1,2,1],[1,2,1]) == True
assert is_Sub_Array([1,0,2,2],[2,2,0]) ==False

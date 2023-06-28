"""
Write a python function to count the number of pairs whose xor value is odd.
"""

def find_Odd_Pair(A,N) : 
    oddPair = 0
    for i in range(0,N) :  
        for j in range(i+1,N) :  
            if ((A[i] ^ A[j]) % 2 != 0):  
                oddPair+=1  
    return oddPair  



assert find_Odd_Pair([5,4,7,2,1],5) == 6
assert find_Odd_Pair([7,2,8,1,0,5,11],7) == 12
assert find_Odd_Pair([1,2,3],3) == 2

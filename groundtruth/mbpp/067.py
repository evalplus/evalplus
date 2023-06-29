"""
Write a function to find the number of ways to partition a set of Bell numbers.
"""

def bell_number(n):   
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    assert n >= 0, "invalid inputs" # $_CONTRACT_$
    bell = [[0 for i in range(n+1)] for j in range(n+1)] 
    bell[0][0] = 1
    for i in range(1, n+1): 
        bell[i][0] = bell[i-1][i-1]  
        for j in range(1, i+1): 
            bell[i][j] = bell[i-1][j-1] + bell[i][j-1]   
    return bell[n][0] 



assert bell_number(2)==2
assert bell_number(10)==115975
assert bell_number(56)==6775685320645824322581483068371419745979053216268760300

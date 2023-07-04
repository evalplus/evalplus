"""
Write a function that takes in a list and an integer n and splits a list for every nth element, returning a list of the resulting lists.
"""

def list_split(S, step):
    assert isinstance(S, list), "invalid inputs" # $_CONTRACT_$
    assert isinstance(step, int), "invalid inputs" # $_CONTRACT_$
    return [S[i::step] for i in range(step)]



assert list_split(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n'],3)==[['a', 'd', 'g', 'j', 'm'], ['b', 'e', 'h', 'k', 'n'], ['c', 'f', 'i', 'l']]
assert list_split([1,2,3,4,5,6,7,8,9,10,11,12,13,14],3)==[[1,4,7,10,13], [2,5,8,11,14], [3,6,9,12]]
assert list_split(['python','java','C','C++','DBMS','SQL'],2)==[['python', 'C', 'DBMS'], ['java', 'C++', 'SQL']]

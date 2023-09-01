"""
Write a function to find the difference of the first even and first odd number of a given list.
"""

def diff_even_odd(list1):
    assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(i, int) for i in list1), "invalid inputs" # $_CONTRACT_$
    assert any(el%2==0 for el in list1), "invalid inputs" # $_CONTRACT_$
    assert any(el%2!=0 for el in list1), "invalid inputs" # $_CONTRACT_$
    first_even = next((el for el in list1 if el%2==0), -1)
    first_odd = next((el for el in list1 if el%2!=0), -1)
    return (first_even - first_odd)



assert diff_even_odd([1,3,5,7,4,1,6,8])==3
assert diff_even_odd([1,2,3,4,5,6,7,8,9,10])==1
assert diff_even_odd([1,5,7,9,10])==9

"""
Write a python function to check whether the given array is monotonic or not.
"""

def is_Monotonic(A): 
    assert isinstance(A, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(item, (int, float)) for item in A), "invalid inputs" # $_CONTRACT_$
    return all(a <= b for a, b in zip(A, A[1:])) or all(a >= b for a, b in zip(A, A[1:]))



assert is_Monotonic([6, 5, 4, 4]) == True
assert is_Monotonic([1, 2, 2, 3]) == True
assert is_Monotonic([1, 3, 2]) == False

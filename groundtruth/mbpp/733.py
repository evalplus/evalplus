"""
Write a function to find the index of the first occurrence of a given number in a sorted array.
"""

def find_first_occurrence(A, x):
    assert isinstance(A, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(a, (int, float)) for a in A), "invalid inputs" # $_CONTRACT_$
    assert all(a <= b for a, b in zip(A, A[1:])), "invalid inputs" # $_CONTRACT_$
    assert isinstance(x, int), "invalid inputs" # $_CONTRACT_$
    (left, right) = (0, len(A) - 1)
    result = -1
    while left <= right:
        mid = (left + right) // 2
        if x == A[mid]:
            result = mid
            right = mid - 1
        elif x < A[mid]:
            right = mid - 1
        else:
            left = mid + 1
    return result



assert find_first_occurrence([2, 5, 5, 5, 6, 6, 8, 9, 9, 9], 5) == 1
assert find_first_occurrence([2, 3, 5, 5, 6, 6, 8, 9, 9, 9], 5) == 2
assert find_first_occurrence([1, 2, 4, 5, 6, 6, 8, 9, 9, 9], 6) == 4

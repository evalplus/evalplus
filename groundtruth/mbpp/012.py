"""
Write a function to sort a given matrix in ascending order according to the sum of its rows.
"""

def sort_matrix(M):
    assert isinstance(M, list), "invalid inputs" # $_CONTRACT_$
    assert len(M) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(row, list) for row in M), "invalid inputs" # $_CONTRACT_$
    assert len(M[0]) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(len(row) == len(M[0]) for row in M), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(item, (int, float)) for row in M for item in row), "invalid inputs" # $_CONTRACT_$
    result = sorted(M, key=sum)
    return result



assert sort_matrix([[1, 2, 3], [2, 4, 5], [1, 1, 1]])==[[1, 1, 1], [1, 2, 3], [2, 4, 5]]
assert sort_matrix([[1, 2, 3], [-2, 4, -5], [1, -1, 1]])==[[-2, 4, -5], [1, -1, 1], [1, 2, 3]]
assert sort_matrix([[5,8,9],[6,4,3],[2,1,4]])==[[2, 1, 4], [6, 4, 3], [5, 8, 9]]

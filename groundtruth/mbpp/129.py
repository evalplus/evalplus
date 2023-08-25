"""
Write a function to calculate whether the matrix is a magic square.
"""

def magic_square_test(my_matrix):
    assert isinstance(my_matrix, list), "invalid inputs" # $_CONTRACT_$
    assert len(my_matrix) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(row, list) for row in my_matrix), "invalid inputs" # $_CONTRACT_$
    assert len(my_matrix[0]) > 0, "invalid inputs" # $_CONTRACT_$
    assert all(len(row) == len(my_matrix[0]) for row in my_matrix), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(item, (int, float)) for row in my_matrix for item in row), "invalid inputs" # $_CONTRACT_$
    s = sum(my_matrix[0])
    # row
    if any(sum(row) != s for row in my_matrix):
        return False
    # column
    if any(sum(row[i] for row in my_matrix) != s for i in range(len(my_matrix[0]))):
        return False
    # diagonal
    if sum(my_matrix[i][i] for i in range(len(my_matrix))) != s:
        return False
    # anti-diagonal
    if sum(my_matrix[i][len(my_matrix) - i - 1] for i in range(len(my_matrix))) != s:
        return False
    return True



assert magic_square_test([[7, 12, 1, 14], [2, 13, 8, 11], [16, 3, 10, 5], [9, 6, 15, 4]])==True
assert magic_square_test([[2, 7, 6], [9, 5, 1], [4, 3, 8]])==True
assert magic_square_test([[2, 7, 6], [9, 5, 1], [4, 3, 7]])==False

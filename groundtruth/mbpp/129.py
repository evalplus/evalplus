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
    iSize = len(my_matrix[0])
    sum_list = []
    sum_list.extend([sum (lines) for lines in my_matrix])   
    for col in range(iSize):
        sum_list.append(sum(row[col] for row in my_matrix))
    result1 = 0
    for i in range(0,iSize):
        result1 +=my_matrix[i][i]
    sum_list.append(result1)      
    result2 = 0
    for i in range(iSize-1,-1,-1):
        result2 +=my_matrix[i][i]
    sum_list.append(result2)
    if len(set(sum_list))>1:
        return False
    return True



assert magic_square_test([[7, 12, 1, 14], [2, 13, 8, 11], [16, 3, 10, 5], [9, 6, 15, 4]])==True
assert magic_square_test([[2, 7, 6], [9, 5, 1], [4, 3, 8]])==True
assert magic_square_test([[2, 7, 6], [9, 5, 1], [4, 3, 7]])==False

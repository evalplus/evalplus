"""
Write a function to sort a given list of strings of numbers numerically. https://www.geeksforgeeks.org/python-sort-numeric-strings-in-a-list/
"""

def sort_numeric_strings(nums_str):
    assert isinstance(nums_str, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(x, str) for x in nums_str), "invalid inputs" # $_CONTRACT_$
    assert all(num.lstrip('-').rstrip(' ').isdigit for num in nums_str), "invalid inputs" # $_CONTRACT_$
    result = [int(x) for x in nums_str]
    result.sort()
    return result



assert sort_numeric_strings( ['4','12','45','7','0','100','200','-12','-500'])==[-500, -12, 0, 4, 7, 12, 45, 100, 200]
assert sort_numeric_strings(['2','3','8','4','7','9','8','2','6','5','1','6','1','2','3','4','6','9','1','2'])==[1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 5, 6, 6, 6, 7, 8, 8, 9, 9]
assert sort_numeric_strings(['1','3','5','7','1', '3','13', '15', '17','5', '7 ','9','1', '11'])==[1, 1, 1, 3, 3, 5, 5, 7, 7, 9, 11, 13, 15, 17]

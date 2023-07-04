"""
Write a function to sort the given array by using shell sort.
"""

def shell_sort(my_list):
    assert isinstance(my_list, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(ele, (int, float)) for ele in my_list), "invalid inputs" # $_CONTRACT_$
    gap = len(my_list) // 2
    while gap > 0:
        for i in range(gap, len(my_list)):
            current_item = my_list[i]
            j = i
            while j >= gap and my_list[j - gap] > current_item:
                my_list[j] = my_list[j - gap]
                j -= gap
            my_list[j] = current_item
        gap //= 2

    return my_list



assert shell_sort([12, 23, 4, 5, 3, 2, 12, 81, 56, 95]) == [2, 3, 4, 5, 12, 12, 23, 56, 81, 95]
assert shell_sort([24, 22, 39, 34, 87, 73, 68]) == [22, 24, 34, 39, 68, 73, 87]
assert shell_sort([32, 30, 16, 96, 82, 83, 74]) == [16, 30, 32, 74, 82, 83, 96]

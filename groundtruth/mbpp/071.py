"""
Write a function to sort a list of elements.
"""

def comb_sort(nums):
    assert isinstance(nums, list), "invalid inputs" # $_CONTRACT_$
    assert all(isinstance(item, (int, float)) for item in nums), "invalid inputs" # $_CONTRACT_$
    shrink_fact = 1.3
    gaps = len(nums)
    swapped = True
    i = 0
    while gaps > 1 or swapped:
        gaps = int(float(gaps) / shrink_fact)
        swapped = False
        i = 0
        while gaps + i < len(nums):
            if nums[i] > nums[i+gaps]:
                nums[i], nums[i+gaps] = nums[i+gaps], nums[i]
                swapped = True
            i += 1
    return nums



assert comb_sort([5, 15, 37, 25, 79]) == [5, 15, 25, 37, 79]
assert comb_sort([41, 32, 15, 19, 22]) == [15, 19, 22, 32, 41]
assert comb_sort([99, 15, 13, 47]) == [13, 15, 47, 99]

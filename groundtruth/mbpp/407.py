"""
Write a function to create the next bigger number by rearranging the digits of a given number.
"""

def rearrange_bigger(n):
    assert isinstance(n, int), "invalid inputs" # $_CONTRACT_$
    nums = list(str(n))
    for i in range(len(nums)-2,-1,-1):
        if nums[i] < nums[i+1]:
            z = nums[i:]
            y = min(filter(lambda x: x > z[0], z))
            z.remove(y)
            z.sort()
            nums[i:] = [y] + z
            return int("".join(nums))
    return False



assert rearrange_bigger(12)==21
assert rearrange_bigger(10)==False
assert rearrange_bigger(102)==120

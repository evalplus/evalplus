"""
Write a function to subtract two lists element-wise.
"""

def sub_list(nums1,nums2):
  assert isinstance(nums1, list), "invalid inputs" # $_CONTRACT_$
  assert isinstance(nums2, list), "invalid inputs" # $_CONTRACT_$
  assert len(nums1) > 0, "invalid inputs" # $_CONTRACT_$
  assert len(nums2) > 0, "invalid inputs" # $_CONTRACT_$
  assert len(nums1) == len(nums2), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(num, (int, float)) for num in nums1), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(num, (int, float)) for num in nums2), "invalid inputs" # $_CONTRACT_$
  return [num1 - num2 for num1, num2 in zip(nums1, nums2)]



assert sub_list([1, 2, 3],[4,5,6])==[-3,-3,-3]
assert sub_list([1,2],[3,4])==[-2,-2]
assert sub_list([90,120],[50,70])==[40,50]

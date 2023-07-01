"""
Write a function to subtract two lists element-wise.
"""

def sub_list(nums1,nums2):
  assert isinstance(nums1, list), "invalid inputs" # $_CONTRACT_$
  assert isinstance(nums2, list), "invalid inputs" # $_CONTRACT_$
  result = map(lambda x, y: x - y, nums1, nums2)
  return list(result)



assert sub_list([1, 2, 3],[4,5,6])==[-3,-3,-3]
assert sub_list([1,2],[3,4])==[-2,-2]
assert sub_list([90,120],[50,70])==[40,50]

"""
Write a function to divide two lists element wise.
"""

def div_list(nums1,nums2):
  assert isinstance(nums1, list), "invalid inputs" # $_CONTRACT_$
  assert isinstance(nums2, list), "invalid inputs" # $_CONTRACT_$
  assert len(nums1) > 0, "invalid inputs" # $_CONTRACT_$
  assert len(nums2) > 0, "invalid inputs" # $_CONTRACT_$
  assert len(nums1) == len(nums2), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, (int, float)) for x in nums1 + nums2), "invalid inputs" # $_CONTRACT_$
  assert all(x != 0 for x in nums2), "invalid inputs" # $_CONTRACT_$
  result = map(lambda x, y: x / y, nums1, nums2)
  return list(result)



assert div_list([4,5,6],[1, 2, 3])==[4.0,2.5,2.0]
assert div_list([3,2],[1,4])==[3.0, 0.5]
assert div_list([90,120],[50,70])==[1.8, 1.7142857142857142]

"""
Write a function to convert all possible convertible elements in a list of lists to floats.
"""

def list_to_float(test_list):
  assert isinstance(test_list, list), "invalid inputs" # $_CONTRACT_$
  assert len(test_list) > 0, "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, list) for x in test_list), "invalid inputs" # $_CONTRACT_$
  assert all(len(x) > 0 for x in test_list), "invalid inputs" # $_CONTRACT_$
  res = []
  for l in test_list:
    t = []
    for e in l:
      try:
        t.append(float(e))
      except:
        t.append(e)
    res.append(t)
  return res



assert list_to_float( [["3", "4"], ["1", "26.45"], ["7.32", "8"], ["4", "8"]] ) == [[3.0, 4.0], [1.0, 26.45], [7.32, 8.0], [4.0, 8.0]]
assert list_to_float( [["4", "4"], ["2", "27"], ["4.12", "9"], ["7", "11"]] ) == [[4.0, 4.0], [2.0, 27.0], [4.12, 9.0], [7.0, 11.0]]
assert list_to_float( [["6", "78"], ["5", "26.45"], ["1.33", "4"], ["82", "13"]] ) == [[6.0, 78.0], [5.0, 26.45], [1.33, 4.0], [82.0, 13.0]]

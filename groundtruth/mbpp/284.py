"""
Write a function that takes in a list and element and checks whether all items in the list are equal to the given element.
"""

def check_element(list1, element):
  assert isinstance(list1, list), "invalid inputs" # $_CONTRACT_$
  assert all(isinstance(x, type(element)) for x in list1), "invalid inputs" # $_CONTRACT_$
  return all(v == element for v in list1)



assert check_element(["green", "orange", "black", "white"],'blue')==False
assert check_element([1,2,3,4],7)==False
assert check_element(["green", "green", "green", "green"],'green')==True

"""
Write a function that takes in a list and element and checks whether all items in the list are equal to the given element.
"""

def check_element(list,element):
  check_element=all(v== element for v in list)
  return check_element



assert check_element(["green", "orange", "black", "white"],'blue')==False
assert check_element([1,2,3,4],7)==False
assert check_element(["green", "green", "green", "green"],'green')==True
